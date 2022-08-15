from typing import Optional
from uuid import UUID

from elasticsearch_dsl import Q, Search


def _get_search(
    query: Optional[str] = None,
    sort: str = '-imdb_rating',
    page_num: int = 1,
    page_size: int = 50,
    _filter: Optional[UUID] = None,
) -> Search:
    """
    Получение Search.

    Args:
        query: Параметр поиска.
        sort: Параметр сортировки.
        page_num: Номер страницы.
        page_size: Размер страницы.
        _filter: Параметр фильтрации по жанрам.

    Returns:
        Search: Объект Search.
    """
    search = Search(index='movies').query('match_all').sort(sort)
    if _filter:
        search = search.query('bool', filter=[Q('terms', tags=['genre', str(_filter)])])
    if query:
        start = (page_num - 1) * page_size
        stop = page_size * page_num
        search = search.query('multi_match', query=query, fuzziness='auto')[start:stop]
    return search


if __name__ == '__main__':
    body = _get_search(query='None', sort='-None', page_num=1, page_size=50, _filter=None)