# === r7kit/child.py ===
from __future__ import annotations

import uuid as _uuid
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Union

from temporalio.common import RetryPolicy

from .tasks import create_task
from .workflow_utils import call_child, start_child

_TASKFLOW_QUEUE_ATTR = "__r7kit_queue__"


@dataclass(frozen=True, slots=True)
class _ChildHelper:                   # noqa: D101
    wf:      Union[str, type]
    task_id: str
    queue:   str | None = None
    retry:   RetryPolicy | Mapping[str, Any] | None = None
    id_:     str | None = None

    # ───────── execute (await result) ──────────
    async def run(self, *args: Any, **kwargs: Any):
        return await call_child(
            self.wf,
            self.task_id,
            *args,
            queue=self.queue,
            retry=self.retry,
            id_=self.id_,
            **kwargs,
        )

    # ───────── fire-and-forget / handle ────────
    async def start(                  # noqa: PLR0913
        self,
        *args: Any,
        payload: dict | None = None,
        memo:   dict | None = None,
        search: dict | None = None,
        uuid:   str  | None = None,
        **kwargs: Any,
    ):
        if payload is not None:
            task_id = await create_task(payload, uuid=uuid)
            wf_args = [task_id, *args]
        else:
            task_id = None
            wf_args = [self.task_id, *args]

        handle = await start_child(
            self.wf,
            *wf_args,
            queue=self.queue,
            retry=self.retry,
            id_=self.id_,
            memo=memo,
            search=search,
            **kwargs,
        )
        return (handle, task_id) if payload is not None else handle


# ───────── фабрика, привязанная к task_id ─────────
def child(
    wf: Union[str, type],
    *,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_: str | None = None,
) -> Callable[[str], _ChildHelper]:
    def _factory(task_id: str) -> _ChildHelper:
        if isinstance(wf, type) and hasattr(wf, _TASKFLOW_QUEUE_ATTR):
            default_q = getattr(wf, _TASKFLOW_QUEUE_ATTR)
        else:
            default_q = None
        return _ChildHelper(
            wf=wf,
            task_id=task_id,
            queue=queue or default_q,
            retry=retry,
            id_=id_,
        )

    return _factory
