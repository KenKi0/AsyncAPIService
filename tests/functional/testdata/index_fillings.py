import uuid

import pytest

film_ids_1 = [str(uuid.uuid4()) for _ in range(20)]
film_ids_2 = [str(uuid.uuid4()) for _ in range(30)]

movies = [
    {
        'id': film_id,
        'imdb_rating': 8.5,
        'genre': [
            {'id': 'g111', 'name': 'Action'},
            {'id': 'g222', 'name': 'Sci-Fi'},
        ],
        'title': 'The Man',
        'description': 'Man',
        'director': [
            {'id': 'p000', 'name': 'Stan'},
        ],
        'actors_names': ['Ann'],
        'writers_names': ['Ben'],
        'actors': [
            {'id': 'p111', 'name': 'Ann'},
        ],
        'writers': [
            {'id': 'p333', 'name': 'Ben'},
        ],
    }
    for film_id in film_ids_1
]

movies_2 = [
    {
        'id': film_id,
        'imdb_rating': 8.5,
        'genre': [
            {'id': 'g333', 'name': 'Drama'},
        ],
        'title': 'The Shawshank Redemption',
        'description': 'Jail break',
        'director': [
            {'id': 'p000', 'name': 'Stan'},
        ],
        'actors_names': ['Bob'],
        'writers_names': ['Howard', 'Ann'],
        'actors': [
            {'id': 'p222', 'name': 'Bob'},
        ],
        'writers': [
            {'id': 'p111', 'name': 'Ann'},
            {'id': 'p444', 'name': 'Howard'},
        ],
    }
    for film_id in film_ids_2
]

movies.extend(movies_2)

genres = [
    {'id': 'g111', 'name': 'Action', 'description': 'Description'},
    {'id': 'g222', 'name': 'Sci-Fi', 'description': 'Description'},
    {'id': 'g333', 'name': 'Drama', 'description': 'Description'},
]

persons = [
    {'id': 'p000', 'full_name': 'Stan', 'role': 'director', 'film_ids': film_ids_1 + film_ids_2},
    {'id': 'p111', 'full_name': 'Ann', 'role': 'director', 'film_ids': film_ids_1 + film_ids_2},
    {'id': 'p222', 'full_name': 'Bob', 'role': 'director', 'film_ids': film_ids_2},
    {'id': 'p333', 'full_name': 'Ben', 'role': 'director', 'film_ids': film_ids_1},
    {'id': 'p444', 'full_name': 'Howard', 'role': 'director', 'film_ids': film_ids_2},
]


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
