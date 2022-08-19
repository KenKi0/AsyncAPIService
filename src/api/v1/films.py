from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.requests import Request

from models.film import DetailFilmResponse, FilmResponse
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/', response_model=list[FilmResponse])
async def film_response(
    request: Request,
    sort: str,
    film_service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]'),
    page_size: int = Query(default=50, alias='page[size]'),
    _filter: Optional[UUID] = Query(default=None, alias='filter[genre]'),
) -> Optional[list[FilmResponse]]:
    url = str(request.url.include_query_params())
    films = await film_service.get_by_search(
        sort=sort,
        page_size=page_size,
        page_num=page_num,
        _filter=_filter,
        url=url,
    )  # TODO проверить индекс
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return films


@router.get('/search', response_model=list[FilmResponse])
async def search_film_response(
    request: Request,
    query: str,
    film_service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]'),
    page_size: int = Query(default=50, alias='page[size]'),
) -> Optional[list[FilmResponse]]:
    url = str(request.url.include_query_params())
    films = await film_service.get_by_search(
        query=query,
        page_num=page_num,
        page_size=page_size,
        url=url,
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return films


@router.get('/{film_id}', response_model=DetailFilmResponse)
async def film_details(
    request: Request,
    film_id: str,
    film_service: FilmService = Depends(get_film_service),
) -> DetailFilmResponse:
    url = str(request.url.include_query_params())
    film = await film_service.get_by_id(film_id=film_id, url=url)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film
