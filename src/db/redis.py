from typing import Optional

from aioredis import Redis

from core.config import settings

redis: Optional[Redis] = Redis(host=settings.redis.HOST)


async def get_redis() -> Redis:
    return redis
