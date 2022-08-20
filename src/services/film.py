from functools import lru_cache
from typing import Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import DetailFilmResponse, Film, FilmResponse
from models.genre import FilmGenre
from models.person import FilmPerson
from services.utils import ElasticMixin, RedisCacheMixin, SearchMixin


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

    async def get_by_id(self, film_id: str, url: str) -> Optional[DetailFilmResponse]:
        """Получение и запись информации о фильме.
        Args:
            film_id: id фильма.
            url: Ключ для кеша.
        Returns:
            Optional[DetailFilmResponse]: Объект модели DetailFilmResponse | None.
        """

        cached_film = await self.get_from_cache(url)
        if cached_film:
            return DetailFilmResponse.parse_raw(cached_film)
        doc = await self.get_by_id_from_elastic(film_id)
        if doc is None:
            return
        data = Film(**doc['_source'])
        genre_list = (
            [FilmGenre(uuid=item.get('id'), name=item.get('name')) for item in data.genre] if data.genre else []
        )
        actors_list = (
            [FilmPerson(uuid=item.get('id'), full_name=item.get('name')) for item in data.actors] if data.actors else []
        )
        writers_list = (
            [FilmPerson(uuid=item.get('id'), full_name=item.get('name')) for item in data.writers]
            if data.writers
            else []
        )
        directors_list = (
            [FilmPerson(uuid=item.get('id'), full_name=item.get('name')) for item in data.director]
            if data.director
            else []
        )
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
        await self.put_into_cache(key=url, data=film.json())
        return film

    async def get_by_search(self, url: str, **kwargs) -> Optional[list[FilmResponse]]:
        """
        Получение и запись списка данных о фильмах.
        Args:
            url: Ключ для кеша.
            **kwargs: Параметры запроса.
        Returns:
            Optional[list[FilmResponse]]: Список объектов модели FilmResponse | None.
        """

        cached_films = await self.get_from_cache(url)
        if cached_films:
            cached_films = orjson.loads(cached_films)
            return [FilmResponse(**film) for film in cached_films]
        search = self.get_search(
            kwargs.get('query'),
            kwargs.get('sort'),
            kwargs.get('page_num'),
            kwargs.get('page_size'),
            kwargs.get('_filter'),
        )
        docs = await self.get_by_search_from_elastic(search)
        if docs is None:
            return
        data = [Film(**row['_source']) for row in docs['hits']['hits']]
        films = [FilmResponse(uuid=row.id, title=row.title, imdb_rating=row.imdb_rating) for row in data]
        data = orjson.dumps([film.dict() for film in films])
        await self.put_into_cache(url, data)
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
