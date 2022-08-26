import pytest
from testdata.index_fillings import movies


@pytest.fixture
def person_by_id_exepted():
    return {
        'uuid': 'p777',
        'full_name': 'Joe',
        'role': ['actor', 'director'],
        'film_ids': ['f000', 'f111', 'f222'],
    }


@pytest.fixture
def person_films_exepted():
    return [
        {
            'uuid': film.get('id'),
            'title': film.get('title'),
            'imdb_rating': film.get('imdb_rating'),
        }
        for film in movies
    ][0:20]
