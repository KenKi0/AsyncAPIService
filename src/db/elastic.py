from elasticsearch import AsyncElasticsearch

from core.config import settings

es: AsyncElasticsearch | None = AsyncElasticsearch(hosts=settings.elastic.hosts)


async def get_elastic() -> AsyncElasticsearch:
    return es
