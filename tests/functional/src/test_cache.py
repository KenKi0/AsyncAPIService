import pytest
from testdata import index_fillings as es_test_data


@pytest.fixture
def film_cache_exepted():
    return [
        {
            'uuid': film.get('id'),
            'title': film.get('title'),
            'imdb_rating': film.get('imdb_rating'),
        }
        for film in es_test_data.movies
    ]


@pytest.fixture
def genre_cache_exepted():
    return {
        'uuid': es_test_data.genres[0].get('id'),
        'name': es_test_data.genres[0].get('name'),
        'description': es_test_data.genres[0].get('description'),
    }


@pytest.fixture
def person_cache_exepted():
    return [
        {
            'uuid': film.get('id'),
            'title': film.get('title'),
            'imdb_rating': film.get('imdb_rating'),
        }
        for film in es_test_data.movies
    ][0:20]


@pytest.mark.asyncio
async def test_cache(
    make_get_request,
    es_write_data,
    es_drop_data,
    genre_cache_exepted,
):
    """Поиск в кеше."""

    # Запись данных в Elasticsearch
    await es_write_data(
        index='movies',
        data=es_test_data.movies,
    )
    await es_write_data(
        index='genres',
        data=es_test_data.genres,
    )
    await es_write_data(
        index='persons',
        data=es_test_data.persons,
    )

    # Запись данных в кеш
    genre_id = es_test_data.genres[0].get('id')
    async with make_get_request(
        handler_url=f'/api/v1/genres/{genre_id}',
    ) as response:
        assert response.status == 200

    async with make_get_request(
        handler_url='/api/v1/films/',
        query_data={'sort': '-imdb_rating'},
    ) as response:
        assert response.status == 200

    person_id = '26e83050-29ef-4163-a99d-b546cac208f8'
    async with make_get_request(
        handler_url=f'/api/v1/persons/{person_id}/film',
    ) as response:
        assert response.status == 200

    # Удаление данных из Elasticsearch
    await es_drop_data(index='movies')
    await es_drop_data(index='genres')
    await es_drop_data(index='persons')

    # Проверка удаления данных из Elasticsearch
    genre_id = es_test_data.genres[1].get('id')
    async with make_get_request(
        handler_url=f'/api/v1/genres/{genre_id}',
    ) as response:
        assert response.status == 500

    async with make_get_request(
        handler_url='/api/v1/films/',
        query_data={'sort': 'imdb_rating'},
    ) as response:
        assert response.status == 500

    person_id = 'b5d2b63a-ed1f-4e46-8320-cf52a32be358'
    async with make_get_request(
        handler_url=f'/api/v1/persons/{person_id}/film',
    ) as response:
        assert response.status == 500

    # Проверка наличия данных в кеше
    genre_id = es_test_data.genres[0].get('id')
    async with make_get_request(
        handler_url=f'/api/v1/genres/{genre_id}',
    ) as response:
        assert response.status == 200
        body = await response.json()
        assert len(body) == len(genre_cache_exepted), 'Проверка количества полей.'
        assert body == genre_cache_exepted, 'Проверка соответствия данных.'

    async with make_get_request(
        handler_url='/api/v1/films/',
        query_data={'sort': '-imdb_rating'},
    ) as response:
        assert response.status == 200

    person_id = '26e83050-29ef-4163-a99d-b546cac208f8'
    async with make_get_request(
        handler_url=f'/api/v1/persons/{person_id}/film',
    ) as response:
        assert response.status == 200
