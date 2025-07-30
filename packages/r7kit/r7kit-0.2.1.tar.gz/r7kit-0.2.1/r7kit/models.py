# === ПУТЬ К ФАЙЛУ: models.py ===
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, Field, field_validator


class TaskModel(BaseModel, extra="allow", arbitrary_types_allowed=True):
    uuid:        str
    status:      str
    created_at:  datetime
    updated_at:  datetime
    deleted_at:  datetime | None = Field(None)
    payload:     Dict[str, Any] | None = None

    @field_validator("created_at", "updated_at", "deleted_at", mode="before")
    @classmethod
    def _auto_dt(cls, v):
        # pydantic-2 сам умеет ISO-строки, но sandbox даёт str→str,
        # поэтому принудительно пытаемся сконвертить
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                pass
        return v

    @property
    def exists(self) -> bool:
        return self.deleted_at is None
