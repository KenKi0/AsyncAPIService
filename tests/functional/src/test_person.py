import pytest
from testdata import index_fillings as es_test_data
from testdata.persons import person_by_id_exepted  # noqa: F401


@pytest.mark.asyncio
async def test_person_by_id(make_get_request, es_write_data, person_by_id_exepted):  # noqa: F811
    """Поиска по id."""

    await es_write_data(
        index='persons',
        data=es_test_data.persons,
    )
    async with make_get_request(
        handler_url='/api/v1/persons/',
        _id='p777',
    ) as response:

        assert response.status == 200
        body = await response.json()
        assert len(body) == len(person_by_id_exepted), 'Проверка количества полей'
        assert body == person_by_id_exepted, 'Проверка соответствия данных'

    async with make_get_request(
        handler_url='/api/v1/persons/',
        _id='f000-000-000-000-000',
    ) as response:

        assert response.status == 404, 'Проверка поиска по несуществующему id.'
