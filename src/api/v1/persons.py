from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from models.film import FilmResponse
from models.person import DetailPerson
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/search', response_model=list[DetailPerson])
async def search_person_response(
    query: str,
    person_service: PersonService = Depends(get_person_service),
    page_num: int = Query(default=1, alias='page[number]'),
    page_size: int = Query(default=50, alias='page[size]'),
) -> Optional[list[DetailPerson]]:
    """
        Ручка для
        GET /api/v1/persons/search?query=captain&page[number]=1&page[size]=50

    {
      "uuid": "uuid",
      "full_name": "str",
      "role": "str",
      "film_ids": ["uuid"]
    }
    ...
    """

    person = await person_service.get_by_search(
        query=query,
        page_num=page_num,
        page_size=page_size,
    )
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/{person_id}', response_model=DetailPerson)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> DetailPerson:
    """
        Ручка для
        GET /api/v1/persons/<uuid:UUID>

    {
      "uuid": "uuid",
      "full_name": "str",
      "role": "str",
      "film_ids": ["uuid"]
    }
    """

    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/{person_id}/film', response_model=list[FilmResponse])
async def person_films(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
) -> list[FilmResponse]:
    """
    Ручка для
    GET /api/v1/persons/<uuid:UUID>/film
    """
    sort = '-imdb_rating'
    person_films = await person_service.get_by_search(sort=sort, _person=person_id)
    if not person_films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return person_films
