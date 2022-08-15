from functools import lru_cache
from typing import Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from fastapi import Depends

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import DetailFilmResponse, Film, FilmResponse

from .utils import create_key

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

    async def get_by_id(self, film_id: str) -> Optional[DetailFilmResponse]:
        """Получение и запись информации о фильме.

        Args:
            film_id: id фильма.

        Returns:
            Optional[Film]: Объект модели Film | None.
        """

        film = await self._film_from_cache(film_id)
        if not film:
            try:
                data = await self._get_film_from_elastic(film_id)
                film = DetailFilmResponse(
                    uuid=data.id,
                    title=data.title,
                    imdb_rating=data.imdb_rating,
                    description=data.description,
                    genre=data.genre,
                    actors=data.actors,
                    writers=data.writers,
                    directors=data.director,
                )
            except NotFoundError as ex:  # noqa: F841
                #  TODO logging
                return None
            await self._put_film_to_cache(film)
        return film

    async def get_by_search(self, search: Search) -> Optional[list[FilmResponse]]:
        """
        Получение и запись списка данных о фильмах.

        Args:
            search: Объект класса Search.

        Returns:
            Optional[list[FilmResponse]]: Список объектов модели FilmResponse | None.
        """

        query = search.to_dict()
        key = create_key(str(query))
        films = await self._search_from_cache(key)
        if not films:
            try:
                data = await self._get_search_from_elastic(search)
                films = [FilmResponse(uuid=row.id, title=row.title, imdb_rating=row.imdb_rating) for row in data]
            except NotFoundError as ex:  # noqa: F841
                #  TODO logging
                return None
            await self._put_search_to_cache(key, films)
        return films

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        """Получение данных о фильме из Elasticsearch.

        Args:
            film_id: id фильма.

        Returns:
            Optional[Film]: Объект модели Film | None.
        """

        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError as ex:  # noqa: F841
            #  TODO logging
            return None
        return Film(**doc['_source'])

    async def _get_search_from_elastic(self, search: Search) -> Optional[list[Film]]:
        """
        Получение списка данных о фильмах из Elasticsearch.

        Args:
            search: Объект класса Search.

        Returns:
            Optional[list[Film]]: Список объектов модели Film | None.
        """

        try:
            query = search.to_dict()
            index = search.index[0]
            data = await self.elastic.search(index=index, body=query)
            hits = data['hits']['hits']
            films = [Film(**row('_source')) for row in hits]
        except NotFoundError as ex:  # noqa: F841
            #  TODO logging
            return None
        return films

    async def _film_from_cache(
        self,
        key: str,
    ) -> Optional[DetailFilmResponse]:
        """Получение данных о фильме из Redis.

        Args:
            key: Ключ.

        Returns:
            Optional[Film]: Объект модели Film | None.
        """

        data = await self.redis.get(key)
        if not data:
            return None
        return DetailFilmResponse.parse_raw(data)

    async def _search_from_cache(self, key: str) -> Optional[list[FilmResponse]]:
        """Получение списка данных о фильмах из Redis.

        Args:
            key: ключ.

        Returns:
            Optional[list[FilmResponse]]:
                Список объектов модели FilmResponse | None.
        """
        data = await self.redis.get(key)
        if not data:
            return None
        return [FilmResponse.parse_raw(film) for film in data]

    async def _put_film_to_cache(self, film: DetailFilmResponse) -> None:
        """Запись данных о фильме в кеш.

        Args:
            film: Объект модели DetailFilmResponse.
        """

        await self.redis.set(film.id, film.json(), ex=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_search_to_cache(self, key: str, films: list[FilmResponse]) -> None:
        """Запись данных о фильмах в кеш.

        Args:
            films: Объект модели Film.
            key: Ключ.
        """

        data = orjson.dumps([film.dict() for film in films])
        await self.redis.set(key, data, ex=FILM_CACHE_EXPIRE_IN_SECONDS)


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


if __name__ == '__main__':
    ...
