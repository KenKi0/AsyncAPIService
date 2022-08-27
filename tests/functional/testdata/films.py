import pytest
from testdata.index_fillings import movies


@pytest.fixture
def film_by_id_exepted():
    return {
        'uuid': movies[0].get('id'),
        'title': 'The Man',
        'imdb_rating': 8.5,
        'description': 'Man',
        'genre': [
            {'uuid': '6c162475-c7ed-4461-9184-001ef3d9f26e', 'name': 'Action'},
            {'uuid': 'fb58fd7f-7afd-447f-b833-e51e45e2a778', 'name': 'Sci-Fi'},
        ],
        'actors': [{'uuid': '26e83050-29ef-4163-a99d-b546cac208f8', 'full_name': 'Ann'}],
        'writers': [{'uuid': 'e039eedf-4daf-452a-bf92-a0085c68e156', 'full_name': 'Ben'}],
        'directors': [{'uuid': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'full_name': 'Stan'}],
    }


@pytest.fixture
def film_full_exepted():
    return [
        {
            'uuid': film.get('id'),
            'title': film.get('title'),
            'imdb_rating': film.get('imdb_rating'),
        }
        for film in movies
    ]


@pytest.fixture
def film_pagination_exepted():
    def key(rating):
        return -rating['imdb_rating']

    return sorted(
        [
            {
                'uuid': film.get('id'),
                'title': film.get('title'),
                'imdb_rating': film.get('imdb_rating'),
            }
            for film in movies
        ],
        key=key,
    )
