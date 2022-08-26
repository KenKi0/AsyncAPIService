import uuid

film_ids_1 = [str(uuid.uuid4()) for _ in range(20)]
film_ids_2 = [str(uuid.uuid4()) for _ in range(30)]

movies = [
    {
        'id': film_id,
        'imdb_rating': 8.5,
        'genre': [
            {'id': '6c162475-c7ed-4461-9184-001ef3d9f26e', 'name': 'Action'},
            {'id': 'fb58fd7f-7afd-447f-b833-e51e45e2a778', 'name': 'Sci-Fi'},
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
            {'id': '120a21cf-9097-479e-904a-13dd7198c1dd', 'name': 'Drama'},
        ],
        'title': 'The Shawshank Redemption',
        'description': 'Jail break man',
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
    {'id': '6c162475-c7ed-4461-9184-001ef3d9f26e', 'name': 'Action', 'description': 'Description'},
    {'id': 'fb58fd7f-7afd-447f-b833-e51e45e2a778', 'name': 'Sci-Fi', 'description': 'Description'},
    {'id': '120a21cf-9097-479e-904a-13dd7198c1dd', 'name': 'Drama', 'description': 'Description'},
]

persons = [
    {'id': 'p000', 'full_name': 'Stan', 'role': 'director', 'film_ids': film_ids_1 + film_ids_2},
    {'id': 'p111', 'full_name': 'Ann', 'role': 'director', 'film_ids': film_ids_1 + film_ids_2},
    {'id': 'p222', 'full_name': 'Bob', 'role': 'director', 'film_ids': film_ids_2},
    {'id': 'p333', 'full_name': 'Ben', 'role': 'director', 'film_ids': film_ids_1},
    {'id': 'p444', 'full_name': 'Howard', 'role': 'director', 'film_ids': film_ids_2},
]
