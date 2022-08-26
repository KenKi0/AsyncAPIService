from functools import lru_cache

from fastapi import Depends

from core.logger import logger as _logger
from db.repository import Repository, get_repository
from models.film import DetailFilmResponse, Film, FilmResponse
from models.genre import FilmGenre
from models.person import FilmPerson
from services.utils import SearchMixin

logger = _logger(__name__)


class FilmService(SearchMixin):
    def __init__(self, repo: Repository):
        """
        :param repo:  класс реализущией интерфейс Repository
        """
        self.repo = repo

    async def get_by_id(self, film_id: str, url: str) -> DetailFilmResponse | None:
        """
        Получение и запись информации о фильме.
        :param film_id: id фильма
        :param url: Ключ для кеша
        :return: Объект модели DetailFilmResponse
        """
        doc = await self.repo.get('movies', film_id)
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
        logger.debug('[+] Return film from elastic. url:%s', url)
        return film

    async def get_by_search(self, url: str, **kwargs) -> list[FilmResponse] | None:
        """
        Получение и запись списка данных о фильмах.
        :param url: Ключ для кеша
        :param kwargs: Параметры запроса
        :return: Список объектов модели FilmResponse
        """
        search = self.get_search(
            kwargs.get('query'),
            kwargs.get('sort'),
            kwargs.get('page_num'),
            kwargs.get('page_size'),
            kwargs.get('_filter'),
        )
        docs = await self.repo.search('movies', search)
        if docs is None:
            return
        data = [Film(**row['_source']) for row in docs['hits']['hits']]
        films = [FilmResponse(uuid=row.id, title=row.title, imdb_rating=row.imdb_rating) for row in data]
        logger.debug('[+] Return films from elastic. url:%s', url)
        return films


@lru_cache()
def get_film_service(
    repo: Repository = Depends(get_repository),
) -> FilmService:
    """
    Провайдер для FilmService.
    :param repo: класс реализующий интерфейс Repository
    :return: Объект класса FilmService для API.
    """
    return FilmService(repo)
