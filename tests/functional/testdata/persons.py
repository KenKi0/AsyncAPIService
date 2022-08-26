import pytest


@pytest.fixture
def person_by_id_exepted():
    return {
        'uuid': 'p777',
        'full_name': 'Joe',
        'role': ['actor', 'director'],
        'film_ids': ['f000', 'f111', 'f222'],
    }
