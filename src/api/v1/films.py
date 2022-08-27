from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.utils import SortEnum
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
    sort: SortEnum,
    service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]', ge=1),
    page_size: int = Query(default=50, alias='page[size]', ge=1),
    _filter: UUID | None = Query(default=None, alias='filter[genre]'),
) -> list[FilmResponse] | None:
    films = await service.get_by_search(
        sort=sort,
        page_size=page_size,
        page_num=page_num,
        _filter=_filter,
    )
    if not films:
        logger.debug('[-] %s.', Msg.not_found.value)
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
    query: str,
    service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]', ge=1),
    page_size: int = Query(default=50, alias='page[size]', ge=1),
) -> list[FilmResponse] | None:
    films = await service.get_by_search(
        query=query,
        page_num=page_num,
        page_size=page_size,
    )
    if not films:
        logger.debug('[-] %s. query: %s', Msg.not_found.value, query)
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
    film_id: str,
    service: FilmService = Depends(get_film_service),
) -> DetailFilmResponse | None:
    film = await service.get_by_id(film_id=film_id)
    if not film:
        logger.debug('[-] %s. id: %s', Msg.not_found.value, film_id)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Msg.not_found.value)
    return film
