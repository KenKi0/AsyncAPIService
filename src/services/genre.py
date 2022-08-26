from functools import lru_cache

from fastapi import Depends

from core.logger import logger as _logger
from db.repository import Repository, get_repository
from models.genre import DetailGenre, Genre
from services.utils import SearchMixin

logger = _logger(__name__)


class GenreService(SearchMixin):
    def __init__(self, repo: Repository, index: str = 'genres'):
        """
        :param repo: класс реализующий интерфейс Repository.
        """
        self.repo = repo
        self.index = index  # TODO избавиться от self.index

    async def get(self, uuid: str, url: str) -> DetailGenre | None:
        """
        Получение информации о конкретном жанре
        :param uuid: id жанра в БД
        :param url: Ключ для кеша
        :return: Объект модели DetailGenre
        """
        doc = await self.repo.get('genres', uuid)
        if doc is None:
            return
        elastic_data = Genre(**doc['_source'])
        genre = DetailGenre(uuid=elastic_data.id, name=elastic_data.name, description=elastic_data.description)
        logger.debug('[+] Return genre from elastic. url:%s', url)
        return genre

    async def get_multi(self, url: str) -> list[DetailGenre] | None:
        """
        Получение информации о всех жанрах.
        :param url: Ключ для кеша
        :return: Список объектов модели DetailGenre
        """
        docs = await self.repo.get_multi('genres')
        if docs is None:
            return []
        elastic_data = [Genre(**row['_source']) for row in docs['hits']['hits']]
        genres = [DetailGenre(uuid=row.id, name=row.name, description=row.description) for row in elastic_data]
        logger.debug('[+] Return genres from elastic. url:%s', url)
        return genres


@lru_cache()
def get_genre_service(
    repo: Repository = Depends(get_repository),
) -> GenreService:
    """
    Провайдер для GenreService.
    :param repo: класс реализующий интерфейс Repository
    :return: Объект класса GenreService для API
    """
    return GenreService(repo)
