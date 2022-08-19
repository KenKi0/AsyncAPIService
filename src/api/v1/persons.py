from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.requests import Request

from models.film import FilmResponse
from models.person import DetailPerson
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/search', response_model=list[DetailPerson])
async def search_person_response(
    request: Request,
    query: str,
    person_service: PersonService = Depends(get_person_service),
    page_num: int = Query(default=1, alias='page[number]'),
    page_size: int = Query(default=50, alias='page[size]'),
) -> Optional[list[DetailPerson]]:
    index = 'persons'
    url = str(request.url.include_query_params())
    person = await person_service.get_person_by_search(
        query=query,
        page_num=page_num,
        page_size=page_size,
        index=index,
        url=url,
    )
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/{person_id}', response_model=DetailPerson)
async def person_details(
    request: Request,
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
) -> DetailPerson:
    url = str(request.url.include_query_params())
    person = await person_service.get_by_id(person_id=person_id, url=url)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/{person_id}/film', response_model=list[FilmResponse])
async def person_films(
    request: Request,
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
) -> list[FilmResponse]:
    sort = '-imdb_rating'
    index = 'movies'
    url = str(request.url.include_query_params())
    person_films = await person_service.get_film_person_by_search(index=index, sort=sort, _person=person_id, url=url)
    if not person_films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return person_films
