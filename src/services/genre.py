from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.logger import logger as _logger
from db.elastic import get_elastic
from models.genre import DetailGenre, Genre
from services.utils import ElasticMixin, SearchMixin

logger = _logger(__name__)


class GenreService(SearchMixin, ElasticMixin):
    def __init__(self, elastic: AsyncElasticsearch, index: str = 'genres'):
        """
        Args:
            elastic: Соединение с Elasticsearch.
        """

        self.elastic = elastic
        self.index = index

    async def get(self, uuid: str, url: str) -> DetailGenre | None:
        """Получение информации о конкретном жанре.

        Args:
            uuid: id фильма.
            url: url запроса для кеша

        Returns:
            Optional[DetailGenre]: Объект модели DetailGenre | None.
        """
        doc = await self.get_by_id_from_elastic(uuid)
        if doc is None:
            return
        elastic_data = Genre(**doc['_source'])
        genre = DetailGenre(uuid=elastic_data.id, name=elastic_data.name, description=elastic_data.description)
        logger.debug('[+] Return genre from elastic. url:%s', url)
        return genre

    async def get_multi(self, url: str) -> list[DetailGenre] | None:
        """Получение информации о всех жанрах.

        Args:
            url: url запроса для кеша

        Returns:
            Optional[list[DetailGenre]]: Список объектов модели DetailGenre | None.
        """
        docs = await self.get_multi_from_elastic()
        if docs is None:
            return []
        elastic_data = [Genre(**row['_source']) for row in docs['hits']['hits']]
        genres = [DetailGenre(uuid=row.id, name=row.name, description=row.description) for row in elastic_data]
        logger.debug('[+] Return genres from elastic. url:%s', url)
        return genres


@lru_cache()
def get_genre_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    """Провайдер для FilmService.

    Args:
        elastic: Соединение с Elasticsearch.

        Returns:
            FilmService: Объект класса FilmService для API.
    """

    return GenreService(elastic)
