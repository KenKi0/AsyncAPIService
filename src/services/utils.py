from hashlib import md5

from aioredis import Redis

from core.config import settings


class RedisCacheMixin:
    async def get_from_cache(self, redis: Redis, key: str):
        """
        Bla bla
        :param redis:
        :param key:
        :return:
        """
        data = await redis.get(key)
        if not data:
            return None
        return data

    async def put_into_cache(
        self,
        redis: Redis,
        key: str,
        data: str | bytes,
        ex: int = settings.FILM_CACHE_EXPIRE_IN_SECONDS,
    ) -> None:
        await redis.set(key, data, ex=ex)


def create_key(params: str) -> str:
    """Получение хешированного ключа для Redis.

    Args:
        params: Данные для хеширования.

    Returns:
        str: Хешированный ключ для Redis.
    """

    return md5(params.encode()).hexdigest()  # noqa: DUO130
