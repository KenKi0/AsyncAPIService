from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.requests import Request

from core.config import settings
from core.logger import logger as _logger
from models.film import DetailFilmResponse, FilmResponse
from services.film import FilmService, get_film_service

logger = _logger(__name__)
router = APIRouter()


@router.get('/', response_model=list[FilmResponse])
async def film_response(
    request: Request,
    sort: str,
    film_service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]', ge=1),
    page_size: int = Query(default=50, alias='page[size]', ge=1),
    _filter: UUID | None = Query(default=None, alias='filter[genre]'),
) -> list[FilmResponse] | None:
    url = str(request.url.include_query_params())
    films = await film_service.get_by_search(
        sort=sort,
        page_size=page_size,
        page_num=page_num,
        _filter=_filter,
        url=url,
    )
    if not films:
        logger.debug(f'[-] {settings.film_msg}. url:{url}')  # noqa: PIE803
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=settings.film_msg)
    return films


@router.get('/search', response_model=list[FilmResponse])
async def search_film_response(
    request: Request,
    query: str,
    film_service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]', ge=1),
    page_size: int = Query(default=50, alias='page[size]', ge=1),
) -> list[FilmResponse] | None:
    url = str(request.url.include_query_params())
    films = await film_service.get_by_search(
        query=query,
        page_num=page_num,
        page_size=page_size,
        url=url,
    )
    if not films:
        logger.debug(f'[-] {settings.film_msg}. url:{url}')  # noqa: PIE803
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=settings.film_msg)
    return films


@router.get('/{film_id}', response_model=DetailFilmResponse)
async def film_details(
    request: Request,
    film_id: str,
    film_service: FilmService = Depends(get_film_service),
) -> DetailFilmResponse | None:
    url = str(request.url.include_query_params())
    film = await film_service.get_by_id(film_id=film_id, url=url)
    if not film:
        logger.debug(f'[-] {settings.film_msg}. url:{url}')  # noqa: PIE803
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=settings.film_msg)
    return film
