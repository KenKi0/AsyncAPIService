import pytest
from testdata import index_fillings as es_test_data


class BaseTest:
    """Поиск по id."""

    index: str = 'movies'
    data_id: list[dict] = es_test_data.film
    handler_url: str = '/api/v1/films/'
    _id: str = 'f111'

    @pytest.mark.asyncio
    async def test_data_by_id(self, make_get_request_by_id, es_write_data):
        """Проверка поиска по id."""

        await es_write_data(self.index, self.data_id)
        response = await anext(make_get_request_by_id(self.handler_url, self._id))

        assert response.status == 200
        body = await response.json()
        assert len(body) == 1


class BaseSearchTest(BaseTest):
    """Поиск по query."""

    index_search: str = 'movies'
    data_query: list[dict] = es_test_data.movies
    handler_url_search: str = '/api/v1/films/search/'
    query: dict = {'query': 'Star'}
    _len: int = 20

    @pytest.mark.asyncio
    async def test_search_data(self, make_get_request_by_search, es_write_data):
        """Проверка поиска фильмов по названию."""

        await es_write_data(self.index_search, self.data_query)
        response = await anext(make_get_request_by_search(self.handler_url_search, self.query))

        assert response.status == 200
        body = await response.json()
        assert len(body) >= self._len
