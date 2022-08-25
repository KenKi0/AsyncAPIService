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
            {
                'uuid': 'g111',
                'name': 'Action',
            },
            {
                'uuid': 'g222',
                'name': 'Sci-Fi',
            },
        ],
        'actors': [
            {
                'uuid': 'p111',
                'full_name': 'Ann',
            },
        ],
        'writers': [
            {
                'uuid': 'p333',
                'full_name': 'Ben',
            },
        ],
        'directors': [
            {
                'uuid': 'p000',
                'full_name': 'Stan',
            },
        ],
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
