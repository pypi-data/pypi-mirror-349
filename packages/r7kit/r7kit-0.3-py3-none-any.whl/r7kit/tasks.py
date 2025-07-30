# === ПУТЬ К ФАЙЛУ: r7kit/tasks.py ===
from __future__ import annotations

import asyncio
from contextlib import suppress
from datetime import timedelta
from typing import Any, Mapping, Optional, Sequence, Union, overload

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.workflow import _NotInWorkflowEventLoopError

from .activities   import (
    RedisOnly,
    create_act,
    delete_act,
    get_act,
    patch_act,
)
from .exceptions   import TaskNotFoundError
from .models       import TaskModel
from .redis_client import get_redis_client          # ← new
from .serializer   import dumps, loads

_DEFAULT_TO = timedelta(seconds=30)

# ───────────────────── helpers ───────────────────────────────────────
def _inside_workflow() -> bool:
    """Возвращает True, если код исполняется внутри WF event-loop."""
    with suppress(_NotInWorkflowEventLoopError):
        workflow.info()            # бросит ошибку, если вне WF
        return True
    return False


async def _unwrap(obj: Any) -> Any:
    """Заменяет RedisOnly → оригинальный объект (рекурсивно)."""
    if isinstance(obj, RedisOnly):
        return loads(obj.value) if isinstance(obj.value, str) else obj.value
    if isinstance(obj, list):
        return [await _unwrap(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(await _unwrap(v) for v in obj)
    if isinstance(obj, Mapping):
        return {k: await _unwrap(v) for k, v in obj.items()}
    return obj


def _resolve_path(obj: Any, path: str, *, default: Any = ...):
    """Достаёт значение по точечному пути (dict + list/tuple)."""
    cur: Any = obj
    for part in path.split("."):
        if isinstance(cur, Mapping):
            if part not in cur:
                if default is ...:
                    raise KeyError(f"{path!r}: ключ {part!r} не найден")
                return default
            cur = cur[part]
            continue
        if isinstance(cur, (list, tuple)):
            try:
                idx = int(part)
            except ValueError:
                raise KeyError(f"{path!r}: {part!r} не индекс списка") from None
            if idx >= len(cur):
                if default is ...:
                    raise KeyError(f"{path!r}: индекс {idx} вне диапазона")
                return default
            cur = cur[idx]
            continue
        if default is ...:
            raise KeyError(f"{path!r}: путь обрывается на неподдерживаемом типе")
        return default
    return cur


# ───────────────────────── CRUD wrappers ─────────────────────────────
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


async def patch_task(
    task_id: str,
    patch: dict[str, Any],
    *,
    stream: str | None = None,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> None:
    if not patch:
        raise ValueError("patch должен быть непустым словарём")

    safe_patch = {k: await _unwrap(v) for k, v in patch.items()}

    if _inside_workflow():
        # локальная activity, чтобы большие данные не шли через gRPC
        await workflow.execute_local_activity(
            patch_act,
            args=[task_id, safe_patch, stream],
            start_to_close_timeout=timeout or _DEFAULT_TO,
            retry_policy=retry_policy,
        )
    else:
        # вызов «снаружи» не нужен; пусть бросит
        raise RuntimeError("patch_task можно вызывать только из воркфлоу")


async def delete_task(
    task_id: str,
    *,
    stream: str | None = None,
    ttl: int | None = None,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> None:
    if _inside_workflow():
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


# mini-DSL для произвольных activity (без изменений)
from temporalio import workflow as _wf  # noqa: E402


async def act(
    name: str,
    *activity_args: Any,
    timeout: int | None = None,
    **activity_kwargs: Any,
) -> Any:
    to = timedelta(seconds=timeout) if timeout else _DEFAULT_TO
    return await _wf.execute_activity(
        name,
        *activity_args,
        **activity_kwargs,
        start_to_close_timeout=to,
    )


# ─────────────────── raw-fetch + parsing (WF и outside) ──────────────
async def _raw_task(task_id: str) -> Optional[dict[str, str]]:
    if _inside_workflow():
        return await workflow.execute_activity(
            get_act,
            args=[task_id],
            start_to_close_timeout=_DEFAULT_TO,
            retry_policy=RetryPolicy(maximum_attempts=1),
        )
    # --- снаружи WF ---------------------------------------------------
    cli = await get_redis_client()
    return await cli.hgetall(f"task:{task_id}") or None


def _parse_task(raw: dict[str, str]) -> TaskModel:
    parsed = {k: loads(v) for k, v in raw.items()}

    meta_keys = {"uuid", "status", "created_at", "updated_at", "deleted_at", "ver"}

    # 1) business-часть, кроме служебных полей и самого "payload"
    business: dict[str, Any] = {
        k: v for k, v in parsed.items()
        if k not in meta_keys and k != "payload"
    }

    # 2) если в хэше есть поле "payload" (словарь/объект) — распаковываем внутрь
    pay = parsed.get("payload")
    if isinstance(pay, Mapping):
        business.update(pay)
    elif pay is not None:
        # не словарь – сохраняем как есть
        business["payload"] = pay

    return TaskModel.model_validate(
        {
            "uuid":       parsed["uuid"],
            "status":     parsed["status"],
            "created_at": parsed["created_at"],
            "updated_at": parsed["updated_at"],
            "deleted_at": parsed.get("deleted_at"),
            "payload":    business or None,
        }
    )


# ────────────────────── get_task & params (универсальные) ────────────
async def get_task(
    task_id: str,
    *,
    timeout: Optional[timedelta] = None,
) -> TaskModel | None:
    raw = await _raw_task(task_id)
    return _parse_task(raw) if raw else None


@overload
async def get_task_params(
    task_id: str,
    path: str,
    *,
    default: Any = ...,
) -> Any: ...
@overload
async def get_task_params(
    task_id: str,
    *paths: str,
    default: Any = ...,
) -> dict[str, Any]: ...


async def get_task_params(
    task_id: str,
    *paths: str,
    default: Any = ...,
):
    """
    Достаёт интересующие поля как из WF, так и из произвольного кода.
    """
    task = await get_task(task_id)
    if not task:
        raise TaskNotFoundError(task_id)

    src: Mapping[str, Any] = {
        **(task.model_dump(exclude_none=True, exclude={"payload"}) or {}),
        "payload": task.payload or {},
    }

    if len(paths) == 1:
        return _resolve_path(src, paths[0], default=default)

    return {p: _resolve_path(src, p, default=default) for p in paths}
