# === r7kit/tasks.py ==========================================================
from __future__ import annotations

import asyncio
from contextlib import suppress
from datetime import timedelta
from typing import Any, Mapping, Optional, overload

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.workflow import _NotInWorkflowEventLoopError

from .activities import (
    RedisOnly,
    create_act,
    delete_act,
    get_act,
    patch_act,
)
from .exceptions   import TaskNotFoundError
from .models       import TaskModel
from .redis_client import get_redis_client
from .serializer   import dumps, loads          # ⇐ dumps понадобится в side-effect
from .config       import cfg                   # ⇐ для подключения sync-Redis

# ---------------------------------------------------------------------------
_DEFAULT_TO = timedelta(seconds=30)

# ───────── helpers ─────────────────────────────────────────────────────────
def _inside_wf() -> bool:
    """True, когда код исполняется в контексте Workflow-рентайма."""
    with suppress(_NotInWorkflowEventLoopError):
        workflow.info()
        return True
    return False


async def _unwrap(obj: Any) -> Any:
    """Снимаем RedisOnly и рекурсивно вытаскиваем вложения."""
    if isinstance(obj, RedisOnly):
        return loads(obj.value) if isinstance(obj.value, str) else obj.value
    if isinstance(obj, list):
        return [await _unwrap(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(await _unwrap(v) for v in obj)
    if isinstance(obj, Mapping):
        return {k: await _unwrap(v) for k, v in obj.items()}
    return obj


def _resolve(obj: Any, path: str, *, default: Any = ...):
    """Достаём значение по точечному пути path.a.b[2].c."""
    cur: Any = obj
    for part in path.split("."):
        if isinstance(cur, Mapping):
            if part not in cur:
                if default is ...:
                    raise KeyError(f"{path!r}: ключ {part!r} не найден")
                return default
            cur = cur[part]; continue
        if isinstance(cur, (list, tuple)):
            try:
                idx = int(part)
            except ValueError:
                raise KeyError(f"{path!r}: {part!r} не индекс списка") from None
            if idx >= len(cur):
                if default is ...:
                    raise KeyError(f"{path!r}: индекс {idx} вне диапазона")
                return default
            cur = cur[idx]; continue
        if default is ...:
            raise KeyError(f"{path!r}: неподдерживаемый тип")
        return default
    return cur


# ───────── raw-fetch + parsing ─────────────────────────────────────────────
async def _raw(task_id: str) -> Optional[dict[str, str]]:
    """Возвращает «сырой» Redis-хэш задачи либо None."""
    if _inside_wf():
        return await workflow.execute_activity(
            get_act,
            args=[task_id],
            start_to_close_timeout=_DEFAULT_TO,
            retry_policy=RetryPolicy(maximum_attempts=1),
        )
    cli = await get_redis_client()
    return await cli.hgetall(f"task:{task_id}") or None


def _parse(raw: dict[str, str]) -> TaskModel:
    parsed = {k: loads(v) for k, v in raw.items()}
    meta = {"uuid", "status", "created_at", "updated_at", "deleted_at", "ver"}

    biz: dict[str, Any] = {k: v for k, v in parsed.items()
                           if k not in meta and k != "payload"}
    pay = parsed.get("payload")
    if isinstance(pay, Mapping):
        biz.update(pay)
    elif pay is not None:
        biz["payload"] = pay

    return TaskModel.model_validate(
        {
            "uuid":       parsed["uuid"],
            "status":     parsed["status"],
            "created_at": parsed["created_at"],
            "updated_at": parsed["updated_at"],
            "deleted_at": parsed.get("deleted_at"),
            "payload":    biz or None,
        }
    )

# ───────── CRUD wrappers ───────────────────────────────────────────────────
async def create_task(
    payload: dict[str, Any] | None = None,
    *,
    uuid: str | None = None,
    status: str = "new",
    stream: str | None = None,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> str:
    return await workflow.execute_activity(
        create_act,
        args=[payload, status, stream, uuid],
        start_to_close_timeout=timeout or _DEFAULT_TO,
        retry_policy=retry_policy,
    )


async def patch_task(                      # noqa: PLR0913
    task_id: str,
    patch: dict[str, Any],
    *,
    stream: str | None = None,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> None:
    """
    • Всё, что помечено `redis_only()`, кладётся в Redis локально через
      `workflow.side_effect()` – в history пишется лишь `True`.
    • Остальные «лёгкие» поля патчатся обычной activity `r7kit.patch`.
    """
    if not patch:
        raise ValueError("patch должен быть непустым словарём")

    heavy: dict[str, Any] = {}
    light: dict[str, Any] = {}

    # --- разделяем --------------------------------------------------
    for k, v in patch.items():
        if isinstance(v, RedisOnly):
            heavy[k] = v.value           # bytes | str | json-serializable
        else:
            light[k] = await _unwrap(v)

    # --- heavy → Redis (side-effect) --------------------------------
    if heavy:
        def _store_blob(fields: dict[str, Any]) -> bool:
            import redis                                     # sync-клиент
            r = redis.Redis.from_url(str(cfg().redis_url), decode_responses=False)
            mapping = {
                k: (v if isinstance(v, (str, bytes)) else dumps(v))
                for k, v in fields.items()
            }
            r.hset(f"task:{task_id}", mapping=mapping)
            return True

        # результат (`True`) детерминирован, поэтому реплей пройдёт
        await workflow.side_effect(bool, _store_blob, heavy)

    # --- light → обычный patch_act ----------------------------------
    if light:
        await workflow.execute_local_activity(
            patch_act,
            args=[task_id, light, stream],
            start_to_close_timeout=timeout or _DEFAULT_TO,
            retry_policy=retry_policy,
        )


async def delete_task(
    task_id: str,
    *,
    stream: str | None = None,
    ttl: int | None = None,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> None:
    if _inside_wf():
        await workflow.execute_activity(
            delete_act,
            args=[task_id, stream, ttl],
            start_to_close_timeout=timeout or _DEFAULT_TO,
            retry_policy=retry_policy,
        )
    else:
        cli = await get_redis_client()
        await cli.hset(f"task:{task_id}", mapping={"deleted_at": "now"})
        if ttl:
            await cli.expire(f"task:{task_id}", ttl)


# ───────── public getters ───────────────────────────────────────────
async def get_task(task_id: str,
                   *, timeout: Optional[timedelta] = None
                  ) -> TaskModel | None:
    raw = await _raw(task_id)
    return _parse(raw) if raw else None


@overload
async def get_task_params(task_id: str,
                          path: str,
                          *, default: Any = ...,
                          timeout: Optional[timedelta] | int | None = None
                         ) -> Any: ...
@overload
async def get_task_params(task_id: str,
                          *paths: str,
                          default: Any = ...,
                          timeout: Optional[timedelta] | int | None = None
                         ) -> dict[str, Any]: ...


async def get_task_params(task_id: str,
                          *paths: str,
                          default: Any = ...,
                          timeout: Optional[timedelta] | int | None = None):
    _ = timeout  # оставлено на будущее – сейчас параметры читаются мгновенно
    task = await get_task(task_id)
    if not task:
        raise TaskNotFoundError(task_id)

    root: Mapping[str, Any] = {
        **(task.model_dump(exclude_none=True, exclude={"payload"}) or {}),
        "payload": task.payload or {},
    }

    if len(paths) == 1:
        return _resolve(root, paths[0], default=default)
    return {p: _resolve(root, p, default=default) for p in paths}


# ───────── удобный вызов activity по имени ─────────────────────────
from temporalio import workflow as _wf  # noqa: E402

async def act(name: str,
              *activity_args: Any,
              timeout: int | None = None,
              **activity_kwargs: Any) -> Any:
    """resp = await act("generate", model, prompt, timeout=300)"""
    to = timedelta(seconds=timeout) if timeout else _DEFAULT_TO
    return await _wf.execute_activity(
        name,
        args=list(activity_args) if activity_args else None,
        start_to_close_timeout=to,
        **activity_kwargs,
    )


# -------------------------------------------------------------------
__all__ = (
    "create_task",
    "patch_task",
    "delete_task",
    "get_task",
    "get_task_params",
    "act",
)
