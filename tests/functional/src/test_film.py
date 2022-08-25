import pytest
from testdata import index_fillings as es_test_data
from testdata.index_fillings import film_by_id_exepted  # noqa: F401


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
