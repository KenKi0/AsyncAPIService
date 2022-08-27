import pytest
from testdata import index_fillings as es_test_data
from testdata.persons import person_by_id_exepted, person_films_exepted  # noqa: F401


@pytest.mark.asyncio
async def test_person_by_id(make_get_request, es_write_data, person_by_id_exepted):  # noqa: F811
    """Поиск по id."""

    await es_write_data(
        index='persons',
        data=es_test_data.persons,
    )
    person_id = 'p777'
    async with make_get_request(
        handler_url=f'/api/v1/persons/{person_id}',
    ) as response:

        assert response.status == 200
        body = await response.json()
        assert len(body) == len(person_by_id_exepted), 'Проверка количества полей.'
        assert body == person_by_id_exepted, 'Проверка соответствия данных.'
    wrong_person_id = 'p000-000-000-000-000'
    async with make_get_request(
        handler_url=f'/api/v1/persons/{wrong_person_id}',
    ) as response:

        assert response.status == 404, 'Проверка поиска по несуществующему id.'


@pytest.mark.asyncio
async def test_search_person(make_get_request, es_write_data):
    """Проверка поиска персон по имени."""

    await es_write_data(
        index='persons',
        data=es_test_data.persons,
    )
    async with make_get_request(
        handler_url='/api/v1/persons/search/',
        query_data={'query': 'bob'},
    ) as response:
        assert response.status == 200
        body = await response.json()
        assert len(body) == 2, 'Проверка наличия всех персон (Bob, Boby).'

    async with make_get_request(
        handler_url='/api/v1/persons/search/',
        query_data={'query': 'anny'},
    ) as response:
        assert response.status == 200
        body = await response.json()
        assert len(body) == 1, 'Проверка наличия всех персон (Ann).'


@pytest.mark.asyncio
async def test_person_films_by_id(make_get_request, es_write_data, person_films_exepted):  # noqa: F811
    """Поиск фильмов по id персоны."""

    await es_write_data(
        index='movies',
        data=es_test_data.movies,
    )
    person_id = '26e83050-29ef-4163-a99d-b546cac208f8'
    async with make_get_request(
        handler_url=f'/api/v1/persons/{person_id}/film',
    ) as response:

        assert response.status == 200
        body = await response.json()
        assert len(body) == 50, 'Проверка количества полей (Актер во всех фильмах).'

    person_id = 'e039eedf-4daf-452a-bf92-a0085c68e156'
    async with make_get_request(
        handler_url=f'/api/v1/persons/{person_id}/film',
    ) as response:

        assert response.status == 200
        body = await response.json()
        assert len(body) == 20, 'Проверка количества полей (Сценарист в 20 фильмах).'

        def desc(rating):
            return -rating['imdb_rating']

        assert body == sorted(person_films_exepted, key=desc), 'Проверка соответствия данных.'

    wrong_person_id = 'p000-000-000-000-000'
    async with make_get_request(
        handler_url=f'/api/v1/persons/{wrong_person_id}/film',
    ) as response:

        assert response.status == 404, 'Проверка поиска по несуществующему id.'
