from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        """
        Args:
            redis: Соединение с Redis.
            elastic: Соединение с Elasticsearch.
        """

        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        """Получение и запись информации о фильме.

        Args:
            film_id: id фильма.

        Returns:
            Optional[Film]: Объект модели Film | None.
        """

        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        """Получение данных о фильме из Elasticsearch.

        Args:
            film_id: id фильма.

        Returns:
            Optional[Film]: Объект модели Film | None.
        """

        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        """Получение данных о фильме из Redis.

        Args:
            film_id: id фильма.

        Returns:
            Optional[Film]: Объект модели Film | None.
        """

        data = await self.redis.get(film_id)
        if not data:
            return None

        return Film.parse_raw(data)

    async def _put_film_to_cache(self, film: Film) -> None:
        """Запись данных о фильме в Redis.

        Args:
            film: Объект модели Film.
        """

        await self.redis.set(film.id, film.json(), ex=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    """Провайдер для FilmService.

    Args:
        redis: Соединение с Redis.
        elastic: Соединение с Elasticsearch.

        Returns:
            FilmService: Объект класса FilmService для API.
    """

    return FilmService(redis, elastic)
