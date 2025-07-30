from __future__ import annotations

from datetime import timedelta
from typing import Any, Mapping, Optional, Union

from temporalio.common import RetryPolicy

from .child          import child as _child_factory
from .models         import TaskModel
from .tasks          import (
    delete_task,
    get_task,
    patch_task,
    get_task_params,   # ← NEW
)
from .workflow_utils import call_child, start_child

DEFAULT_TIMEOUT = timedelta(seconds=30)


class BaseWorkflow:
    task_id: str

    def __init__(self) -> None:
        self.task_id = ""

    # ----------------------------------------------------------------
    async def _run_impl(self, task_id: str, *args: Any, **kwargs: Any) -> Any:
        if not task_id:
            raise ValueError("Первый аргумент run() должен быть непустым task_id")
        self.task_id = task_id
        return await self.handle(*args, **kwargs)

    async def handle(self, *args: Any, **kwargs: Any) -> Any:   # noqa: D401
        """Переопределите в наследнике."""
        raise NotImplementedError

    # ──────────────── УДОБНЫЕ SELECTOR-Ы ДАННЫХ ЗАДАЧИ ───────────────
    async def param(self,
                    path: str,
                    *,
                    default: Any = ...,
                    timeout: int | None = None):
        """
        Получить *одно* значение по пути::

            dur = await self.param("payload.audio.duration", default=0)
        """
        return await get_task_params(
            self.task_id,
            path,
            default=default,
            timeout=timedelta(seconds=timeout) if timeout else DEFAULT_TIMEOUT,
        )

    async def params(self,
                     *paths: str,
                     default: Any = ...,
                     timeout: int | None = None):
        """
        Получить сразу несколько значений::

            got = await self.params("status", "payload.foo")
            # → {"status": "...", "payload.foo": ...}
        """
        return await get_task_params(
            self.task_id,
            *paths,
            default=default,
            timeout=timedelta(seconds=timeout) if timeout else DEFAULT_TIMEOUT,
        )

    # ----------------------------------------------------------------
    async def get_task(self, timeout: Optional[timedelta] = None) -> TaskModel | None:
        return await get_task(self.task_id, timeout=timeout or DEFAULT_TIMEOUT)

    async def patch_task(
        self,
        patch: dict[str, Any],
        *,
        timeout: Optional[timedelta] = None,
    ) -> None:
        if not patch:
            raise ValueError("patch должен быть непустым словарём")
        await patch_task(self.task_id, patch, timeout=timeout or DEFAULT_TIMEOUT)

    async def delete_task(
        self,
        *,
        ttl: int | None = None,
        timeout: Optional[timedelta] = None,
    ) -> None:
        """Логическое удаление задачи."""
        await delete_task(
            self.task_id,
            ttl=ttl,
            timeout=timeout or DEFAULT_TIMEOUT,
        )

    async def exists(self) -> bool:
        t = await self.get_task()
        return bool(t and t.exists)

    # ----------------------------------------------------------------
    async def call_child(
        self,
        wf: Union[str, type],
        *args: Any,
        queue: str | None = None,
        retry: RetryPolicy | Mapping[str, Any] | None = None,
        id_: str | None = None,
    ) -> Any:
        return await call_child(
            wf,
            self.task_id,
            *args,
            queue=queue,
            retry=retry,
            id_=id_,
        )

    async def start_child(
        self,
        wf: Union[str, type],
        *args: Any,
        queue: str | None = None,
        retry: RetryPolicy | Mapping[str, Any] | None = None,
        id_: str | None = None,
    ):
        return await start_child(
            wf,
            self.task_id,
            *args,
            queue=queue,
            retry=retry,
            id_=id_,
        )

    def child(
        self,
        wf: Union[str, type],
        *,
        queue: str | None = None,
        retry: RetryPolicy | Mapping[str, Any] | None = None,
        id_: str | None = None,
    ):
        """
        Удобная фабрика::

            my_child = self.child(MyWorkflow)(...)   # ← task_id подставится
        """
        return _child_factory(wf, queue=queue, retry=retry, id_=id_)(self.task_id)
