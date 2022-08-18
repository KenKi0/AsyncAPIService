from functools import lru_cache
from typing import Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from fastapi import Depends

from api.v1.utils import SearchMixin
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import DetailFilmResponse, Film, FilmResponse
from models.genre import DetailGenre
from models.person import FilmPerson
from services.utils import RedisCacheMixin, create_key


class FilmService(SearchMixin, RedisCacheMixin):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index: str = 'movies'):
        """
        Args:
            redis: Соединение с Redis.
            elastic: Соединение с Elasticsearch.
        """

        self.redis = redis
        self.elastic = elastic
        self.index = index

    async def get_by_id(self, film_id: str) -> Optional[DetailFilmResponse]:
        """Получение и запись информации о фильме.

        Args:
            film_id: id фильма.

        Returns:
            Optional[DetailFilmResponse]: Объект модели DetailFilmResponse | None.
        """

        data = await self.get_from_cache(self.redis, film_id)
        film = DetailFilmResponse.parse_raw(data)
        if not film:
            try:
                data = await self._get_film_from_elastic(film_id)
                genre_list = [DetailGenre(uuid=item.get('id'), name=item.get('name')) for item in data.genre]
                actors_list = [FilmPerson(uuid=item.get('id'), full_name=item.get('name')) for item in data.actors]
                writers_list = [FilmPerson(uuid=item.get('id'), full_name=item.get('name')) for item in data.writers]
                directors_list = [FilmPerson(uuid=item.get('id'), full_name=item.get('name')) for item in data.director]
                film = DetailFilmResponse(
                    uuid=data.id,
                    title=data.title,
                    imdb_rating=data.imdb_rating,
                    description=data.description,
                    actors=actors_list,
                    genre=genre_list,
                    writers=writers_list,
                    directors=directors_list,
                )
            except NotFoundError as ex:  # noqa: F841
                #  TODO logging
                return None
            await self.put_into_cache(self.redis, film.uuid, film.json())
        return film

    async def get_by_search(self, **kwargs) -> Optional[list[FilmResponse]]:
        """
        Получение и запись списка данных о фильмах.

        Args:
            search: Объект класса Search.
            key: Запрос к сервису

        Returns:
            Optional[list[FilmResponse]]: Список объектов модели FilmResponse | None.
        """

        search = self.get_search(
            self.index,
            kwargs.get('query'),
            kwargs.get('sort'),
            kwargs.get('page_num'),
            kwargs.get('page_size'),
            kwargs.get('_filter'),
        )
        key = create_key(f'{self.index}:{search.to_dict()}')
        data = await self.get_from_cache(self.redis, key)
        films = [FilmResponse(**film) for film in data]
        if not films:
            try:
                data = await self._get_search_from_elastic(search)
                films = [FilmResponse(uuid=row.id, title=row.title, imdb_rating=row.imdb_rating) for row in data]
            except NotFoundError as ex:  # noqa: F841
                #  TODO logging
                return None
            data = orjson.dumps([film.dict() for film in films])
            await self.put_into_cache(self.redis, key, data)
        return films

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        """Получение данных о фильме из Elasticsearch.

        Args:
            film_id: id фильма.

        Returns:
            Optional[Film]: Объект модели Film | None.
        """

        try:
            doc = await self.elastic.get(self.index, film_id)
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
            data = await self.elastic.search(index=self.index, body=query)
            films = [Film(**row['_source']) for row in data['hits']['hits']]
        except NotFoundError as ex:  # noqa: F841
            #  TODO logging
            return None
        return films


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
