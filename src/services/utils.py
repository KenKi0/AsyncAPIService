from hashlib import md5
from typing import Optional

from elasticsearch import NotFoundError
from elasticsearch_dsl import Q, Search

from core.config import settings
from core.logger import logger as _logger

logger = _logger(__name__)


class SearchMixin:
    def get_search(
        self,
        query: Optional[str] = None,
        sort: Optional[str] = None,
        page_num: int = 1,
        page_size: int = 50,
        _filter: Optional[str] = None,
        _person: Optional[str] = None,
    ) -> Search:
        """
        Получение Search.
        :param query: Параметр поиска.
        :param sort: Параметр сортировки.
        :param page_num: Номер страницы.
        :param page_size: Размер страницы.
        :param _filter: Параметр фильтрации по жанрам.
        :param _person: id персоны.
        :return Search: Объект Search.
        """
        start = (page_num - 1) * page_size
        stop = page_size * page_num
        search = Search(index=self.index).query('match_all')[start:stop]
        if sort:
            search = search.sort(sort)
        if _filter:
            search = search.query('bool', should=[Q('nested', path='genre', query=Q('match', genre__id=_filter))])
        if _person:
            search = search.query(
                'bool',
                should=[
                    Q('nested', path='actors', query=Q('match', actors__id=_person)),
                    Q('nested', path='writers', query=Q('match', writers__id=_person)),
                    Q('nested', path='writers', query=Q('match', writers__id=_person)),
                    Q('nested', path='director', query=Q('match', director__id=_person)),
                ],
            )
        if query:
            search = search.query('multi_match', query=query, fuzziness='auto')
        return search


class RedisCacheMixin:
    async def get_from_cache(self, key: str) -> str | bytes | None:
        """
        Получение данных из кеша.
        :param key: Ключ.
        :return str | bytes | None: Данные из кеша.
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
        :param key: Ключ.
        :param data: Данные для записи.
        :param ex: Время хранения данных.
        """
        logger.debug('[+] Put data into cached. url:%s', key)
        await self.redis.set(key, data, ex=ex)


class ElasticMixin:
    async def get_by_id_from_elastic(self, _id: str) -> dict | None:
        """
        Получение данных из Elasticsearch по id.
        :param _id: id .
        :return dict: Ответ elasticsearch в виде dict | None.
        """

        try:
            doc = await self.elastic.get(self.index, _id)
        except NotFoundError as ex:  # noqa: F841
            logger.info('Trying to get non-existent document with id: %s, in index: %s', _id, self.index)
            return None
        return doc

    async def get_by_search_from_elastic(
        self,
        search: Search,
    ) -> dict | None:
        """
        Получение данных из Elasticsearch по id.
        :param search: Объект класса Search .
        :return dict: Ответ elasticsearch в виде dict | None.
        """

        try:
            query = search.to_dict()
            docs = await self.elastic.search(index=self.index, body=query)
        except NotFoundError as ex:  # noqa: F841
            logger.info('No results found for query: \n%s\nIn index: %s', search.to_dict(), self.index)
            return None
        return docs

    async def get_multi_from_elastic(self) -> dict | None:
        """
        Получение всех данных индекса из Elasticsearch.
        :return dict: Ответ elasticsearch в виде dict | None.
        """
        body = {'query': {'match_all': {}}}
        try:
            doc = await self.elastic.search(index=self.index, body=body)
        except NotFoundError as ex:  # noqa: F841
            logger.info('No results found for all query in index: %s', self.index)
            return None
        return doc


def create_key(params: str) -> str:
    """
    Получение хешированного ключа для Redis.
    :param params: Данные для хеширования.
    :return str: Хешированный ключ для Redis.
    """

    return md5(params.encode()).hexdigest()  # noqa: DUO130
