import pytest
from base import BaseSearchTest
from testdata import index_fillings as es_test_data


class TestFilm(BaseSearchTest):

    # Поиск по id
    index: str = 'movies'
    data_id: list[dict] = es_test_data.film
    handler_url_id: str = '/api/v1/films/'
    _id: str = 'f111'

    #  Поиск по query
    data_query: list[dict] = es_test_data.movies
    handler_url_search: str = '/api/v1/films/search/'
    query: list[dict] = {'query': 'Star'}
    _len: int = 20

    @pytest.mark.asyncio
    async def test_full_films(make_get_request_by_search, es_write_data):
        """Проверка поиска всех фильмов."""

        await es_write_data('movies', es_test_data.movies)
        response = await anext(make_get_request_by_search('/api/v1/films/', {'sort': '-imdb_rating'}))

        assert response.status == 200
        body = await response.json()
        assert len(body) == 40

    @pytest.mark.asyncio
    async def test_pagination_films(make_get_request_by_search, es_write_data):
        """Проверка наличия фильмов на определенной странице."""

        await es_write_data('movies', es_test_data.movies)
        response = await anext(
            make_get_request_by_search('/api/v1/films/', {'sort': '-imdb_rating', 'filter[genre]': 'g222'}),
        )

        assert response.status == 200
        body = await response.json()
        assert len(body) == 20

    @pytest.mark.asyncio
    async def test_filter_films(make_get_request_by_search, es_write_data):
        """Проверка поиска фильмов определенного жанра."""

        await es_write_data('movies', es_test_data.movies)
        response = await anext(
            make_get_request_by_search(
                '/api/v1/films/',
                {
                    'sort': '-imdb_rating',
                    'page[number]': 2,
                    'page[size]': 20,
                },
            ),
        )

        assert response.status == 200
        body = await response.json()
        assert len(body) == 20
