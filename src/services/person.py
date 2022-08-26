from functools import lru_cache

from fastapi import Depends

from core.logger import logger as _logger
from db.repository import Repository, get_repository
from models.film import Film, FilmResponse
from models.person import DetailPerson, Person
from services.utils import SearchMixin

logger = _logger(__name__)


class PersonService(SearchMixin):
    def __init__(self, repo: Repository):
        """
        :param repo: класс реализующий интерфейс Repository
        """
        self.repo = repo

    async def get_by_id(self, url: str, person_id: str) -> DetailPerson | None:
        """
        Получение и запись информации о персоне.
        :param url: Ключ для кеша
        :param person_id: id персоны
        :return: Объект модели DetailPerson
        """
        doc = await self.repo.get('persons', person_id)
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
        :param url: Ключ для кеша
        :param kwargs: Параметры запроса
        :return: Список объектов модели DetailPerson
        """
        search = self.get_search(
            kwargs.get('query'),
            kwargs.get('sort'),
            kwargs.get('page_num'),
            kwargs.get('page_size'),
        )
        docs = await self.repo.search('persons', search)
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
        :param url: Ключ для кеша
        :param kwargs: Параметры запроса
        :return: Список объектов модели FilmResponse
        """
        search = self.get_search(
            sort='-imdb_rating',
            _person=kwargs.get('_person'),
        )
        docs = await self.repo.search('movies', search)
        if docs is None:
            return
        data = [Film(**row['_source']) for row in docs['hits']['hits']]
        person_films = [FilmResponse(uuid=row.id, title=row.title, imdb_rating=row.imdb_rating) for row in data]
        logger.debug('[+] Return person films from elastic. url:%s', url)
        return person_films


@lru_cache()
def get_person_service(
    repo: Repository = Depends(get_repository),
) -> PersonService:
    """
    Провайдер для PersonService.
    :param repo: класс реализующий интерфейс Repository
    :return: Объект класса PersonService
    """
    return PersonService(repo)
