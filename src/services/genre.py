from functools import lru_cache

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.logger import logger as _logger
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import DetailGenre, Genre
from services.utils import ElasticMixin, RedisCacheMixin, SearchMixin

logger = _logger(__name__)


class GenreService(SearchMixin, RedisCacheMixin, ElasticMixin):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index: str = 'genres'):
        """
        Args:
            redis: Соединение с Redis.
            elastic: Соединение с Elasticsearch.
        """

        self.redis = redis
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
        cached_genre = await self.get_from_cache(url)
        if cached_genre:
            logger.debug('[+] Return genre from cached. url:%s', url)  # noqa: PIE803
            return DetailGenre.parse_raw(cached_genre)
        doc = await self.get_by_id_from_elastic(uuid)
        if doc is None:
            return
        elastic_data = Genre(**doc['_source'])
        genre = DetailGenre(uuid=elastic_data.id, name=elastic_data.name, description=elastic_data.description)
        await self.put_into_cache(url, genre.json())
        logger.debug('[+] Return genre from elastic. url:%s', url)  # noqa: PIE803
        return genre

    async def get_multi(self, url: str) -> list[DetailGenre] | None:
        """Получение информации о всех жанрах.

        Args:
            url: url запроса для кеша

        Returns:
            Optional[list[DetailGenre]]: Список объектов модели DetailGenre | None.
        """
        cached_genres = await self.get_from_cache(url)
        if cached_genres:
            logger.debug('[+] Return genres from cached. url:%s', url)  # noqa: PIE803
            cached_genres = orjson.loads(cached_genres)
            return [DetailGenre(**genre) for genre in cached_genres]
        docs = await self.get_multi_from_elastic()
        if docs is None:
            return []
        elastic_data = [Genre(**row['_source']) for row in docs['hits']['hits']]
        genres = [DetailGenre(uuid=row.id, name=row.name, description=row.description) for row in elastic_data]
        data_to_cache = orjson.dumps([genre.dict() for genre in genres])
        await self.put_into_cache(url, data_to_cache)
        logger.debug('[+] Return genres from elastic. url:%s', url)  # noqa: PIE803
        return genres


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    """Провайдер для FilmService.

    Args:
        redis: Соединение с Redis.
        elastic: Соединение с Elasticsearch.

        Returns:
            FilmService: Объект класса FilmService для API.
    """

    return GenreService(redis, elastic)
