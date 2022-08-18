from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from models.film import DetailFilmResponse, FilmResponse
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/', response_model=list[FilmResponse])
async def film_response(
    sort: str,
    film_service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]'),
    page_size: int = Query(default=50, alias='page[size]'),
    _filter: Optional[UUID] = Query(default=None, alias='filter[genre]'),
) -> Optional[list[FilmResponse]]:

    films = await film_service.get_by_search(
        sort=sort,
        page_size=page_size,
        page_num=page_num,
        _filter=_filter,
    )  # TODO проверить индекс
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return films


@router.get('/search', response_model=list[FilmResponse])
async def search_film_response(
    query: str,
    film_service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]'),
    page_size: int = Query(default=50, alias='page[size]'),
) -> Optional[list[FilmResponse]]:

    films = await film_service.get_by_search(
        query=query,
        page_num=page_num,
        page_size=page_size,
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return films


@router.get('/{film_id}', response_model=DetailFilmResponse)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> DetailFilmResponse:

    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film
