# === ПУТЬ К ФАЙЛУ: r7kit/config.py ===
from __future__ import annotations

import os
from functools import lru_cache
from pydantic import BaseModel, Field
import tomllib


def _from_file(key: str, default: str) -> str:
    # lazy‐import pathlib, чтобы Path.home() не вызывался на уровне модуля
    from pathlib import Path  # type: ignore
    cfg_file = Path.home() / ".r7kit.toml"
    if not cfg_file.is_file():
        return default
    try:
        data = tomllib.loads(cfg_file.read_text())
        return data.get(key, default)
    except Exception:
        return default


class Settings(BaseModel):
    redis_url: str = Field(default_factory=lambda: _from_file("redis_url", "redis://localhost:6379"))
    temporal_address: str = Field(default_factory=lambda: _from_file("temporal", "localhost:7233"))
    stream_default: str = Field(default_factory=lambda: _from_file("stream", "tasks_events"))
    deleted_ttl: int = Field(default_factory=lambda: int(_from_file("ttl", "3600")))

    class Config:
        extra = "ignore"
        frozen = True


@lru_cache()
def cfg() -> Settings:
    # явно передаём всё в конструктор, чтобы default_factory для Settings()
    # тоже вызывался в runtime, а не при import
    defaults = Settings()
    return Settings(
        redis_url=os.getenv("REDIS_URL") or defaults.redis_url,
        temporal_address=os.getenv("TEMPORAL_ADDRESS") or defaults.temporal_address,
        stream_default=os.getenv("R7KIT_STREAM") or defaults.stream_default,
        deleted_ttl=int(os.getenv("R7KIT_DELETED_TTL") or defaults.deleted_ttl),
    )


def configure(
    *,
    redis_url: str | None = None,
    temporal_address: str | None = None,
    stream_default: str | None = None,
    deleted_ttl: int | None = None,
) -> None:
    if cfg.cache_info().currsize:
        raise RuntimeError("r7kit уже инициализирован; configure() нужно вызвать раньше")
    if redis_url:
        os.environ["REDIS_URL"] = redis_url
    if temporal_address:
        os.environ["TEMPORAL_ADDRESS"] = temporal_address
    if stream_default:
        os.environ["R7KIT_STREAM"] = stream_default
    if deleted_ttl is not None:
        os.environ["R7KIT_DELETED_TTL"] = str(deleted_ttl)
