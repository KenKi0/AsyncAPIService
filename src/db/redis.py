import aioredis

from core.config import settings

redis: aioredis.Redis | None = aioredis.from_url(settings.redis.url, max_connections=20, decode_responses=True)


async def get_redis() -> aioredis.Redis:
    return redis
