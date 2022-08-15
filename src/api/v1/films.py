from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from models.film import DetailFilmResponse, FilmResponse
from src.services.film import FilmService, get_film_service

from .utils import get_search

router = APIRouter()


@router.get('/', response_model=FilmResponse)
async def film_response(
    sort: str,
    film_service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]'),
    page_size: int = Query(default=50, alias='page[size]'),
    _filter: Optional[UUID] = Query(default=None, alias='filter[genre]'),
) -> Optional[list[FilmResponse]]:
    """Главная страница с фильмами.

    Args:
        sort: Параметр сортировки.
        page_num: Номер страницы.
        page_size: Размер страницы.
        _filter: Параметр фильтрации по жанрам.
        film_service: Провайдер для FilmService.

    Returns:
        Optional[list[FilmResponse]]: Список объектов модели FilmResponse.
    """
    index = 'movies'
    search = get_search(
        sort=sort,
        page_num=page_num,
        page_size=page_size,
        _filter=_filter,
        index=index,
    )
    films = await film_service.get_by_search(search=search)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return films


@router.get('/search', response_model=FilmResponse)
async def search_film_response(
    query: str,
    film_service: FilmService = Depends(get_film_service),
    page_num: int = Query(default=1, alias='page[number]'),
    page_size: int = Query(default=50, alias='page[size]'),
) -> Optional[list[FilmResponse]]:
    """Поиск по фильмам.

    Args:
        query: Параметр поиска.
        page_num: Номер страницы.
        page_size: Размер страницы.
        film_service: Провайдер для FilmService.

    Returns:
        Optional[list[FilmResponse]]: Список объектов модели FilmResponse.
    """
    index = 'movies'
    search = get_search(
        query=query,
        page_num=page_num,
        page_size=page_size,
        index=index,
    )
    films = await film_service.get_by_search(search=search)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return films


@router.get('/{film_id}', response_model=DetailFilmResponse)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> DetailFilmResponse:
    """Полная информация о фильме.

    Args:
        film_id: id фильма.
        film_service: Провайдер для FilmService.

    Returns:
        DetailFilmResponse: Объект модели DetailFilmResponse.
    """

    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film
