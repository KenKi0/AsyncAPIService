from typing import Optional

from elasticsearch_dsl import Q, Search


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

        Args:
            query: Параметр поиска.
            sort: Параметр сортировки.
            page_num: Номер страницы.
            page_size: Размер страницы.
            _filter: Параметр фильтрации по жанрам.
            _person: id персоны.

        Returns:
            Search: Объект Search.
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


if __name__ == '__main__':
    body = SearchMixin.get_search(
        query=None,
        sort='-imdb_rating',
        page_num=1,
        page_size=50,
        _filter='1234',
        index='movies',
    )
