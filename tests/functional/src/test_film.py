import pytest

from testdata import index_fillings as es_test_data


@pytest.mark.asyncio
async def test_film_by_id(make_get_request, es_write_data):
    await es_write_data('movies', es_test_data.movies)
    response = await anext(make_get_request('/api/v1/films/', {'sort': '-imdb_rating'}))

    assert response.status == 200
    body = await response.json()
    assert len(body) == 40
