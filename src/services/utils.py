from hashlib import md5
from typing import Union

from elasticsearch import NotFoundError
from elasticsearch_dsl import Search

from core.config import settings
from core.logger import logger as _logger

logger = _logger(__name__)


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
        logger.debug(f'[+] Put data into cached. url:{key}')  # noqa: PIE803
        await self.redis.set(key, data, ex=ex)


class ElasticMixin:
    async def get_by_id_from_elastic(self, _id: str) -> dict | None:
        """
        Получение данных из Elasticsearch по id.

        Args:
            _id: id .

        Returns:
            dict: Ответ elasticsearch в виде dict | None.
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
    ) -> dict | None:
        """
        Получение данных из Elasticsearch по id.

        Args:
            search: Объект класса Search .

        Returns:
            dict: Ответ elasticsearch в виде dict | None.
        """

        try:
            query = search.to_dict()
            docs = await self.elastic.search(index=self.index, body=query)
        except NotFoundError as ex:  # noqa: F841
            #  TODO logging
            return None
        return docs

    async def get_multi_from_elastic(self) -> dict | None:
        """
        Получение всех данных индекса из Elasticsearch.

        Returns:
            dict: Ответ elasticsearch в виде dict | None.
        """
        body = {'query': {'match_all': {}}}
        try:
            doc = await self.elastic.search(index=self.index, body=body)
        except NotFoundError as ex:  # noqa: F841
            #  TODO logging
            return None
        return doc


def create_key(params: str) -> str:
    """Получение хешированного ключа для Redis.

    Args:
        params: Данные для хеширования.

    Returns:
        str: Хешированный ключ для Redis.
    """

    return md5(params.encode()).hexdigest()  # noqa: DUO130
