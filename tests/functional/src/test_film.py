import pytest
from base import BaseSearchTest
from testdata import index_fillings as es_test_data


class TestFilm(BaseSearchTest):
    # Поиск по id (test_data_by_id)
    index: str = 'movies'
    data_id: list[dict] = es_test_data.film
    handler_url: str = '/api/v1/films/'
    _id: str = 'f111'

    #  ./search (test_search_data)
    index_search: str = 'movies'
    data_query: list[dict] = es_test_data.movies
    handler_url_search: str = '/api/v1/films/search/'
    query: dict = {'query': 'Star'}
    _len: int = 20

    #  Все фильмы (test_full_films)
    query_full: dict = {'sort': '-imdb_rating'}
    _len_full: int = 40

    #  Пагинация
    query_pagination: dict = {'sort': '-imdb_rating', 'filter[genre]': 'g222'}
    _len_pagination: int = 20

    # Фильтр по жанрам (test_filter_films)
    query_filter: dict = {'sort': '-imdb_rating', 'page[number]': 2, 'page[size]': 20}
    _len_filter: int = 20

    @pytest.mark.asyncio
    async def test_full_films(self, make_get_request_by_search, es_write_data):
        """Проверка поиска всех фильмов."""

        await es_write_data(self.index, self.data_query)
        response = await anext(make_get_request_by_search(self.handler_url, self.query_full))

        assert response.status == 200
        body = await response.json()
        assert len(body) == self._len_full

    @pytest.mark.asyncio
    async def test_pagination_films(self, make_get_request_by_search, es_write_data):
        """Проверка наличия фильмов на определенной странице."""

        await es_write_data(self.index, self.data_query)
        response = await anext(
            make_get_request_by_search(self.handler_url, self.query_pagination),
        )

        assert response.status == 200
        body = await response.json()
        assert len(body) == self._len_pagination

    @pytest.mark.asyncio
    async def test_filter_films(self, make_get_request_by_search, es_write_data):
        """Проверка поиска фильмов определенного жанра."""

        await es_write_data(self.index, self.data_query)
        response = await anext(make_get_request_by_search(self.handler_url, self.query_filter))

        assert response.status == 200
        body = await response.json()
        assert len(body) == self._len_filter
