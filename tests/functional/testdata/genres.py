import pytest
from testdata.index_fillings import genres


@pytest.fixture
def genre_by_id_exepted():
    return {
        'uuid': genres[0].get('id'),
        'name': genres[0].get('name'),
        'description': genres[0].get('description'),
    }


@pytest.fixture
def genre_full_exepted():
    return [
        {
            'uuid': genre.get('id'),
            'name': genre.get('name'),
            'description': genre.get('description'),
        }
        for genre in genres
    ]
