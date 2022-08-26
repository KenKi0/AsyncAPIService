from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.logger import logger as _logger
from db.elastic import get_elastic
from models.film import Film, FilmResponse
from models.person import DetailPerson, Person
from services.utils import ElasticMixin, SearchMixin

logger = _logger(__name__)


class PersonService(SearchMixin, ElasticMixin):
    def __init__(self, elastic: AsyncElasticsearch, index: str = 'persons'):
        """
        :param elastic: Соединение с Elasticsearch.
        """

        self.elastic = elastic
        self.index = index

    async def get_by_id(self, url: str, person_id: str, index: str = 'persons') -> DetailPerson | None:
        """
        Получение и запись информации о персоне.
        :param url: Ключ для кеша.
        :param person_id: id персоны.
        :param index: Индекс для Elasticsearch.
        :return Optional[DetailPerson]: Объект модели DetailPerson | None.
        """

        self.index = index
        doc = await self.get_by_id_from_elastic(person_id)
        if doc is None:
            return
        data = Person(**doc['_source'])
        person = DetailPerson(
            uuid=data.id,
            full_name=data.full_name,
            role=data.role,
            film_ids=data.film_ids,
        )
        logger.debug('[+] Return person from elastic. url::%s', url)
        return person

    async def get_person_by_search(self, url: str, **kwargs) -> list[DetailPerson] | None:
        """
        Получение и запись списка данных о фильмах.
        :param url: Ключ для кеша.
        :param **kwargs: Параметры запроса.
        :return Optional[list[DetailPerson]]: Список объектов модели DetailPerson | None.
        """

        search = self.get_search(
            kwargs.get('query'),
            kwargs.get('sort'),
            kwargs.get('page_num'),
            kwargs.get('page_size'),
        )
        self.index = kwargs.get('index')
        docs = await self.get_by_search_from_elastic(search)
        if docs is None:
            return
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
        logger.debug('[+] Return persons from elastic. url:%s', url)
        return persons

    async def get_film_person_by_search(self, url: str, **kwargs) -> list[FilmResponse] | None:
        """
        Получение и запись списка данных о фильмах.
        :param url: Ключ для кеша.
        :param **kwargs: Параметры запроса.
        :return Optional[list[FilmResponse]]: Список объектов модели FilmResponse | None.
        """

        search = self.get_search(
            sort=kwargs.get('sort'),
            _person=kwargs.get('_person'),
        )
        self.index = kwargs.get('index')
        docs = await self.get_by_search_from_elastic(search)
        if docs is None:
            return
        data = [Film(**row['_source']) for row in docs['hits']['hits']]
        person_films = [FilmResponse(uuid=row.id, title=row.title, imdb_rating=row.imdb_rating) for row in data]
        logger.debug('[+] Return person films from elastic. url:%s', url)
        return person_films


@lru_cache()
def get_person_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    """
    Провайдер для PersonService.
    :param elastic: Соединение с Elasticsearch.
    :return PersonService: Объект класса PersonService.
    """

    return PersonService(elastic)
