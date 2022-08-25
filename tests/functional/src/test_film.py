import pytest
from testdata import index_fillings as es_test_data
from testdata.index_fillings import film_by_id_exepted, film_full_exepted, film_pagination_exepted  # noqa: F401


@pytest.mark.asyncio
async def test_film_by_id(make_get_request_by_id, es_write_data, film_by_id_exepted):  # noqa: F811
    """Поиска по id."""

    await es_write_data(
        index='movies',
        data=es_test_data.movies,
    )
    response = await anext(
        make_get_request_by_id(
            handler_url='/api/v1/films/',
            _id=es_test_data.movies[0].get('id'),
        ),
    )

    assert response.status == 200
    body = await response.json()
    assert len(body) == len(film_by_id_exepted), 'Проверка количества полей'
    assert body == film_by_id_exepted, 'Проверка соответствия данных'


@pytest.mark.asyncio
async def test_film_by_wrong_id(make_get_request_by_id, es_write_data):
    """Поиска по несуществующему id."""

    await es_write_data(
        index='movies',
        data=es_test_data.movies,
    )
    response = await anext(
        make_get_request_by_id(
            handler_url='/api/v1/films/',
            _id='f000-000-000-000-000',
        ),
    )

    assert response.status == 404, 'Проверка поиска по несуществующему id.'


@pytest.mark.asyncio
async def test_full_films(make_get_request_by_search, es_write_data, film_full_exepted):  # noqa: F811
    """Поиск всех фильмов."""

    await es_write_data(
        index='movies',
        data=es_test_data.movies,
    )
    response = await anext(
        make_get_request_by_search(
            handler_url='/api/v1/films/',
            query_data={'sort': '-imdb_rating'},
        ),
    )

    assert response.status == 200
    body = await response.json()
    assert len(body) == len(film_full_exepted), 'Проверка наличия всех фильмов.'

    def desc(rating):
        return -rating['imdb_rating']

    assert body == sorted(film_full_exepted, key=desc), 'Проверка соответствия данных (DESC).'

    response = await anext(
        make_get_request_by_search(
            handler_url='/api/v1/films/',
            query_data={'sort': 'imdb_rating'},
        ),
    )

    def asc(rating):
        return rating['imdb_rating']

    body = await response.json()
    assert body == sorted(film_full_exepted, key=asc), 'Проверка соответствия данных (ASC).'


@pytest.mark.asyncio
async def test_pagination_films(make_get_request_by_search, es_write_data, film_pagination_exepted):  # noqa: F811
    """Поиск фильмов на определенной странице."""

    await es_write_data(
        index='movies',
        data=es_test_data.movies,
    )
    response = await anext(
        make_get_request_by_search(
            handler_url='/api/v1/films/',
            query_data={'sort': '-imdb_rating', 'page[number]': 2, 'page[size]': 10},
        ),
    )

    assert response.status == 200
    body = await response.json()
    assert len(body) == len(film_pagination_exepted[10:20]), 'Проверка наличия всех фильмов.'

    def key(rating):
        return -rating['imdb_rating']

    assert body == film_pagination_exepted[10:20], 'Проверка соответствия данных.'
