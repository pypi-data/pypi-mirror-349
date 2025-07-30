# === ПУТЬ К ФАЙЛУ: redis_client.py ===
from __future__ import annotations

import asyncio, logging, time
from typing import Optional, cast

import redis.asyncio as redis
from redis.exceptions import ConnectionError, TimeoutError
from fakeredis.aioredis import FakeRedis                  # type: ignore

from .config import cfg

log = logging.getLogger(__name__)

_HEALTH_CHECK   = 30
_MAX_CONN       = 20
_RETRIES        = 3
_BACKOFF        = 2.0
_BREAK_THRESHOLD= 10           # подряд неудач → уходим в «отпуск»
_BREAK_TIME     = 60           # сек

_POOL_LOCK: asyncio.Lock               = asyncio.Lock()
_POOL:      Optional[redis.ConnectionPool] = None
_LAST_ERROR_TS: float | None           = None


async def _create_pool() -> redis.ConnectionPool:
    return cast(
        redis.ConnectionPool,
        redis.ConnectionPool.from_url(
            str(cfg().redis_url),
            decode_responses=True,
            health_check_interval=_HEALTH_CHECK,
            max_connections=_MAX_CONN,
        ),
    )


def _circuit_open() -> bool:
    return _LAST_ERROR_TS is not None and (time.time() - _LAST_ERROR_TS) < _BREAK_TIME


async def get_redis_client() -> redis.Redis:
    """
    Singleton-клиент с circuit-breaker.  
    Если Redis недоступен и breaker «открыт» — возвращаем FakeRedis для
    unit-тестов, чтобы не падала бизнес-логика.
    """
    global _POOL, _LAST_ERROR_TS
    attempt, sleep_for = 0, 0.0

    while True:
        if _POOL:
            return redis.Redis(connection_pool=_POOL)

        if _circuit_open():
            log.warning("Redis circuit-breaker открыт – используем FakeRedis")
            return cast(redis.Redis, await FakeRedis())

        if sleep_for:
            await asyncio.sleep(sleep_for)

        async with _POOL_LOCK:
            if _POOL:                                # мог появиться
                continue
            try:
                _POOL = await _create_pool()
                client = redis.Redis(connection_pool=_POOL)
                await client.ping()
                log.info("Connected to Redis %s", cfg().redis_url)
                _LAST_ERROR_TS = None
                return client
            except (ConnectionError, TimeoutError) as err:
                _LAST_ERROR_TS = time.time()
                attempt += 1
                if attempt > _RETRIES:
                    raise
                sleep_for = _BACKOFF ** attempt
                log.warning("Redis connect failed (%s), retry in %ss", err, sleep_for)
