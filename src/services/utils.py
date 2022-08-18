from hashlib import md5
from typing import Union

from elasticsearch import NotFoundError
from elasticsearch_dsl import Search

from core.config import settings
from models.film import DetailFilmResponse, Film, FilmResponse
from models.genre import DetailGenre, Genre
from models.person import FilmPerson, Person


class RedisCacheMixin:
    async def get_from_cache(self, key: str) -> Union[str, bytes, None]:
        """
        Получение данных из кеша.

        Args:
            key: Ключ.

        Returns:
            Union[str, bytes, None]: Данные из кеша.
        """
        data = await self.redis.get(key)
        if not data:
            return None
        return data

    async def put_into_cache(
        self,
        key: str,
        data: str | bytes,
        ex: int = settings.FILM_CACHE_EXPIRE_IN_SECONDS,
    ) -> None:
        """
        Запись данных в кеш.

        Args:
            key: Ключ.
            data: Данные для записи.
            ex: Время хранения данных.
        """

        await self.redis.set(key, data, ex=ex)


class ElasticMixin:
    async def get_by_id_from_elastic(self, _id: str) -> Union[Film, Person, Genre, None]:
        """
        Получение данных из Elasticsearch по id.

        Args:
            _id: id .

        Returns:
            Union[Film, Person, Genre, None]: Объект модели ответа | None.
        """

        try:
            doc = await self.elastic.get(self.index, _id)
        except NotFoundError as ex:  # noqa: F841
            #  TODO logging
            return None
        return doc

    async def get_by_search_from_elastic(
        self,
        search: Search,
    ) -> list[Union[FilmResponse, DetailFilmResponse, FilmPerson, DetailGenre, None]]:
        """
        Получение данных из Elasticsearch по id.

        Args:
            search: Объект класса Search .

        Returns:
            list[Union[...]]: Список объектов модели ответа | None.
        """

        try:
            query = search.to_dict()
            docs = await self.elastic.search(index=self.index, body=query)
        except NotFoundError as ex:  # noqa: F841
            #  TODO logging
            return None
        return docs


def create_key(params: str) -> str:
    """Получение хешированного ключа для Redis.

    Args:
        params: Данные для хеширования.

    Returns:
        str: Хешированный ключ для Redis.
    """

    return md5(params.encode()).hexdigest()  # noqa: DUO130
