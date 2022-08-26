from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.requests import Request

from core.logger import logger as _logger
from models.film import DetailFilmResponse, FilmResponse
from services.film import FilmService, get_film_service
from services.response_messages import FilmMessages as Msg

logger = _logger(__name__)
router = APIRouter()


@router.get(
    path='/',
    response_model=list[FilmResponse],
    summary='Главная страница кинопроизведений',
    description='Полный перечень кинопроизведений',
    response_description='Список из названий и рейтингов кинопроизведений',
)
async def films(
    request: Request,
    sort: str,
    service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]', ge=1),
    page_size: int = Query(default=50, alias='page[size]', ge=1),
    _filter: UUID | None = Query(default=None, alias='filter[genre]'),
) -> list[FilmResponse] | None:
    url = str(request.url.include_query_params())
    films = await service.get_by_search(
        sort=sort,
        page_size=page_size,
        page_num=page_num,
        _filter=_filter,
        url=url,
    )
    if not films:
        logger.debug('[-] %s. url:%s', Msg.not_found.value, url)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Msg.not_found.value)
    return films


@router.get(
    path='/search',
    response_model=list[FilmResponse],
    summary='Поиск кинопроизведений',
    description='Полнотекстовый поиск по кинопроизведениям',
    response_description='Список из названий и рейтингов кинопроизведений',
)
async def search_film(
    request: Request,
    query: str,
    service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]', ge=1),
    page_size: int = Query(default=50, alias='page[size]', ge=1),
) -> list[FilmResponse] | None:
    url = str(request.url.include_query_params())
    films = await service.get_by_search(
        query=query,
        page_num=page_num,
        page_size=page_size,
        url=url,
    )
    if not films:
        logger.debug('[-] %s. url:%s', Msg.not_found.value, url)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Msg.not_found.value)
    return films


@router.get(
    path='/{film_id}',
    response_model=DetailFilmResponse,
    summary='Поиск кинопроизведения по ID',
    description='Поиск кинопроизведения по ID',
    response_description='Полная информация о кинопроизведении',
)
async def film_details(
    request: Request,
    film_id: str,
    service: FilmService = Depends(get_film_service),
) -> DetailFilmResponse | None:
    url = str(request.url.include_query_params())
    film = await service.get_by_id(film_id=film_id, url=url)
    if not film:
        logger.debug('[-] %s. url:%s', Msg.not_found.value, url)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Msg.not_found.value)
    return film
