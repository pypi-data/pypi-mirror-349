# === ПУТЬ К ФАЙЛУ: workflow_utils.py ===
from __future__ import annotations

import importlib
from datetime import timedelta
from typing import Any, Mapping, Union, overload

from temporalio import workflow
from temporalio.common import RetryPolicy

from .activities      import create_act
from .config          import cfg
from .exceptions      import TemporalNotConnected
from .redis_client    import get_redis_client
from .temporal_client import get_temporal_client

_TASKFLOW_QUEUE_ATTR = "__r7kit_queue__"           # из @taskflow


# ───────────────────────── retry ────────────────────────────────────
def default_retry_policy(
    *,
    initial_interval: float = 1.0,
    backoff: float = 2.0,
    maximum_interval: float | None = None,
    maximum_attempts: int | None = None,
) -> RetryPolicy:
    return RetryPolicy(
        initial_interval=timedelta(seconds=initial_interval),
        backoff_coefficient=backoff,
        maximum_interval=(
            timedelta(seconds=maximum_interval) if maximum_interval else None
        ),
        maximum_attempts=maximum_attempts or 1,
    )

# ───────────────────── helpers ──────────────────────────────────────
def _try_import(path: str) -> type | None:
    if "." not in path:
        return None
    mod, cls = path.rsplit(".", 1)
    try:
        return getattr(importlib.import_module(mod), cls)
    except Exception:
        return None


@overload
async def _prepare(wf: str,  queue: str | None) -> tuple[str,  str, str]: ...
@overload
async def _prepare(wf: type, queue: str | None) -> tuple[type, str, str]: ...


async def _prepare(wf, queue):
    """Приводим wf-ссылку к (wf_ref, wf_name, task_queue)."""
    if isinstance(wf, str):
        cls     = _try_import(wf)
        wf_ref  = cls or wf
        wf_name = cls.__name__ if cls else wf
    else:
        wf_ref  = wf
        wf_name = wf.__name__

    if isinstance(wf_ref, type) and hasattr(wf_ref, _TASKFLOW_QUEUE_ATTR):
        default_q = getattr(wf_ref, _TASKFLOW_QUEUE_ATTR)
    else:
        default_q = f"{wf_name.lower()}-queue"

    return wf_ref, wf_name, (queue or default_q)

# ───── детерминированные «uuid» (без uuid.uuid4!) ───────────────────
def _rand_hex(bits: int) -> str:
    """Возвращает hex-строку (без 0x) заданной длины (пауза надёжно реплеится)."""
    width = bits // 4
    return f"{workflow.random().getrandbits(bits):0{width}x}"


def _unique_child_id(prefix: str) -> str:
    short = _rand_hex(32)  # 8 hex-символов
    return f"{prefix}-{workflow.info().run_id}-{short}"

# ───── child helpers ────────────────────────────────────────────────
async def start_child(                    # noqa: PLR0913
    wf: Union[str, type],
    *wf_args: Any,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_: str | None = None,
    memo: dict[str, Any] | None = None,
    search: dict[str, Any] | None = None,
) -> workflow.ChildWorkflowHandle:
    wf_ref, wf_name, task_queue = await _prepare(wf, queue)
    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))

    search_attrs = (
        {k: (v if isinstance(v, list) else [v]) for k, v in search.items()}
        if search is not None else None
    )

    return await workflow.start_child_workflow(
        wf_ref,
        id=id_ or _unique_child_id(wf_name.lower()),
        task_queue=task_queue,
        retry_policy=rp,
        memo={k: (bv if isinstance(bv, bytes) else str(bv).encode())
              for k, bv in (memo or {}).items()} or None,
        search_attributes=search_attrs,
        args=list(wf_args) if wf_args else None,
    )


async def call_child(
    wf: Union[str, type],
    *wf_args: Any,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_: str | None = None,
):
    wf_ref, wf_name, task_queue = await _prepare(wf, queue)
    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))
    return await workflow.execute_child_workflow(
        wf_ref,
        id=id_ or _unique_child_id(wf_name.lower()),
        task_queue=task_queue,
        retry_policy=rp,
        args=list(wf_args) if wf_args else None,
    )

# ───── submit root ­workflow (id-ы исправлены) ──────────────────────
async def submit_workflow(                # noqa: PLR0913
    wf: Union[str, type],
    *wf_args: Any,
    payload: dict[str, Any] | None = None,
    status: str = "new",
    task_uuid: str | None = None,
    memo: dict[str, Any] | None = None,
    search: dict[str, Any] | None = None,
    workflow_id: str | None = None,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    workflow_kwargs: dict[str, Any] | None = None,
):
    wf_ref, wf_name, task_queue = await _prepare(wf, queue)

    args: list[Any] = list(wf_args)
    _memo: dict[str, bytes] = {}

    # 1) heavy payload → Redis
    if payload is not None:
        tid = task_uuid or _rand_hex(128)
        await create_act(payload, status, cfg().stream_default, tid)
        args.insert(0, tid)

        size = await (await get_redis_client()).memory_usage(f"task:{tid}") or 0
        _memo["taskSize"] = str(size).encode()

    # 2) лёгкий memo
    if memo:
        for k, v in memo.items():
            _memo[k] = v if isinstance(v, bytes) else str(v).encode()

    # 3) searchAttributes
    search_attrs = (
        {k: (v if isinstance(v, list) else [v]) for k, v in search.items()}
        if search is not None else None
    )

    # 4) старт WF
    try:
        client = await get_temporal_client()
    except Exception as exc:                                # pragma: no cover
        raise TemporalNotConnected(f"Cannot connect to Temporal: {exc}") from exc

    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))
    wf_id = workflow_id or (
        args[0] if payload is not None else f"{wf_name.lower()}-{_rand_hex(32)}"
    )

    return await client.start_workflow(
        wf_ref,
        id=wf_id,
        task_queue=task_queue,
        retry_policy=rp,
        memo=_memo or None,
        search_attributes=search_attrs,
        args=args if args else None,
        **(workflow_kwargs or {}),
    )
