from aioredis import Redis

from core.config import settings

redis: Redis | None = Redis(host=settings.redis.HOST)


async def get_redis() -> Redis:
    return redis
