from functools import lru_cache
from typing import Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from api.v1.utils import SearchMixin
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, FilmResponse
from models.person import DetailPerson, Person
from services.utils import ElasticMixin, RedisCacheMixin, create_key


class PersonService(SearchMixin, RedisCacheMixin, ElasticMixin):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index: str = 'persons'):
        """
        Args:
            redis: Соединение с Redis.
            elastic: Соединение с Elasticsearch.
        """

        self.redis = redis
        self.elastic = elastic
        self.index = index

    async def get_by_id(self, url: str, person_id: str, index: str = 'persons') -> Optional[DetailPerson]:
        """Получение и запись информации о фильме.

        Args:
            url: Ключ для кеша.
            person_id: id персоны.
            index: Индекс для Elasticsearch.

        Returns:
            Optional[DetailPerson]: Объект модели DetailPerson | None.
        """

        cached_film = await self.get_from_cache(url)
        if cached_film:
            return DetailPerson.parse_raw(cached_film)
        try:
            self.index = index
            doc = await self.get_by_id_from_elastic(person_id)
            data = Person(**doc['_source'])
            person = DetailPerson(
                uuid=data.id,
                full_name=data.full_name,
                role=data.role,
                film_ids=data.film_ids,
            )
        except NotFoundError as ex:  # noqa: F841
            #  TODO logging
            return None
        await self.put_into_cache(key=url, data=person.json())
        return person

    async def get_person_by_search(self, **kwargs) -> Optional[list[DetailPerson]]:
        """
        Получение и запись списка данных о фильмах.

        Args:
            **kwargs: Параметры запроса.

        Returns:
            Optional[list[DetailPerson]]: Список объектов модели DetailPerson | None.
        """

        search = self.get_search(
            kwargs.get('query'),
            kwargs.get('sort'),
            kwargs.get('page_num'),
            kwargs.get('page_size'),
        )
        self.index = kwargs.get('index')
        key = create_key(kwargs.get('url'))
        cached_person = await self.get_from_cache(key)
        if cached_person:
            cached_person = orjson.loads(cached_person)
            return [DetailPerson(**person) for person in cached_person]
        try:
            docs = await self.get_by_search_from_elastic(search)
            data = [Person(**row['_source']) for row in docs['hits']['hits']]
            persons = [
                DetailPerson(
                    uuid=row.id,
                    full_name=row.full_name,
                    role=row.role,
                    film_ids=row.film_ids,
                )
                for row in data
            ]
        except NotFoundError as ex:  # noqa: F841
            #  TODO logging
            return None
        data = orjson.dumps([person.dict() for person in persons])
        await self.put_into_cache(key, data)
        return persons

    async def get_film_person_by_search(self, **kwargs) -> Optional[list[FilmResponse]]:
        """
        Получение и запись списка данных о фильмах.

        Args:
            **kwargs: Параметры запроса.
            key: Запрос к сервису

        Returns:
            Optional[list[FilmResponse]]: Список объектов модели FilmResponse | None.
        """

        search = self.get_search(
            sort=kwargs.get('sort'),
            _person=kwargs.get('_person'),
        )
        self.index = kwargs.get('index')
        key = create_key(kwargs.get('url'))
        cached_film_person = await self.get_from_cache(key)
        if cached_film_person:
            cached_film_person = orjson.loads(cached_film_person)
            return [FilmResponse(**film) for film in cached_film_person]
        try:
            docs = await self.get_by_search_from_elastic(search)
            data = [Film(**row['_source']) for row in docs['hits']['hits']]
            person_films = [FilmResponse(uuid=row.id, title=row.title, imdb_rating=row.imdb_rating) for row in data]
        except NotFoundError as ex:  # noqa: F841
            #  TODO logging
            return None
        data = orjson.dumps([film.dict() for film in person_films])
        await self.put_into_cache(key, data)
        return person_films


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    """Провайдер для PersonService.

    Args:
        redis: Соединение с Redis.
        elastic: Соединение с Elasticsearch.

        Returns:
            PersonService: Объект класса PersonService.
    """

    return PersonService(redis, elastic)


if __name__ == '__main__':
    ...
