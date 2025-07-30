# === ПУТЬ К ФАЙЛУ: r7kit/redis_client.py ===
from __future__ import annotations

import asyncio
import logging
from typing import Optional, cast

import redis.asyncio as redis
from redis.exceptions import ConnectionError, TimeoutError

from .config import cfg

logger = logging.getLogger(__name__)

_POOL_LOCK = asyncio.Lock()
_POOL: Optional[redis.ConnectionPool] = None

# Интервал для health‐check (redis пул делает сам свои проверки)
_HEALTH_CHECK_INTERVAL = 30
# Сколько максимум раз пытаться при старте
_MAX_CONNECT_RETRIES = 3
# Базовый коэффициент экспоненциальной задержки
_BACKOFF_BASE = 2.0


async def _create_pool() -> redis.ConnectionPool:
    """
    Создаёт новый ConnectionPool.
    """
    return cast(
        redis.ConnectionPool,
        redis.ConnectionPool.from_url(
            str(cfg().redis_url),
            decode_responses=True,
            health_check_interval=_HEALTH_CHECK_INTERVAL,
            max_connections=20,
        ),
    )


async def get_redis_client() -> redis.Redis:
    """
    Singleton‐клиент Redis с авто-reconnect и экспоненциальным бэкоффом.
    """
    global _POOL
    attempt = 0
    sleep_for = 0.0

    while True:
        if _POOL is not None:
            # Уже есть пул — отдаем новый объект клиента на его основании
            return redis.Redis(connection_pool=_POOL)

        if sleep_for:
            await asyncio.sleep(sleep_for)

        async with _POOL_LOCK:
            # Кто-то мог создать пул, пока мы ждали
            if _POOL is not None:
                continue
            try:
                _POOL = await _create_pool()
                client = redis.Redis(connection_pool=_POOL)
                # Убедимся, что соединение реально работает
                await client.ping()
                logger.info("Connected to Redis at %s", cfg().redis_url)
                return client
            except (ConnectionError, TimeoutError) as err:
                attempt += 1
                if attempt > _MAX_CONNECT_RETRIES:
                    logger.error(
                        "Failed to connect to Redis at %s after %d attempts",
                        cfg().redis_url,
                        attempt,
                    )
                    # После нескольких неудач позволяем ошибке уйти наружу
                    raise
                # Иначе ждем экспоненциально возрастающую задержку и повторяем
                sleep_for = _BACKOFF_BASE ** attempt
                logger.warning(
                    "Redis connect failed (%s), retrying in %.1fs", err, sleep_for
                )


async def close_redis_client() -> None:
    """
    Полностью закрывает пул и сбрасывает singleton.
    """
    global _POOL
    if _POOL is not None:
        await _POOL.disconnect(inuse_connections=True)
        _POOL = None
