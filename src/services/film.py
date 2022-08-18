from functools import lru_cache
from typing import Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from api.v1.utils import SearchMixin
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import DetailFilmResponse, Film, FilmResponse
from models.genre import DetailGenre
from models.person import FilmPerson
from services.utils import ElasticMixin, RedisCacheMixin, create_key


class FilmService(SearchMixin, RedisCacheMixin, ElasticMixin):
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

        cached_film = await self.get_from_cache(film_id)
        if cached_film:
            return DetailFilmResponse.parse_raw(cached_film)
        try:
            doc = await self.get_by_id_from_elastic(film_id)
            data = Film(**doc['_source'])
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
        await self.put_into_cache(film.uuid, film.json())
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
            kwargs.get('query'),
            kwargs.get('sort'),
            kwargs.get('page_num'),
            kwargs.get('page_size'),
            kwargs.get('_filter'),
        )
        key = create_key(f'{self.index}:{search.to_dict()}')
        cached_films = await self.get_from_cache(key)
        if cached_films:
            return [FilmResponse(**film) for film in cached_films]
        try:
            docs = await self.get_by_search_from_elastic(search)
            data = [Film(**row['_source']) for row in docs['hits']['hits']]
            films = [FilmResponse(uuid=row.id, title=row.title, imdb_rating=row.imdb_rating) for row in data]
        except NotFoundError as ex:  # noqa: F841
            #  TODO logging
            return None
        data = orjson.dumps([film.dict() for film in films])
        await self.put_into_cache(key, data)
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
