from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from core.config import settings
from core.logger import logger as _logger
from models.genre import DetailGenre
from services.genre import GenreService, get_genre_service

logger = _logger(__name__)
router = APIRouter()


@router.get('/{uuid}', response_model=DetailGenre)
async def get_genre(
    uuid: str,
    request: Request,
    service: GenreService = Depends(get_genre_service),
) -> DetailGenre | None:
    genre = await service.get(uuid, str(request.url.include_query_params()))
    if not genre:
        url = str(request.url.include_query_params())
        logger.debug(f'[-] {settings.genre_msg}. url:{url}')  # noqa: PIE803
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=settings.genre_msg)
    return genre


@router.get('/', response_model=list[DetailGenre])
async def get_genres(
    request: Request,
    service: GenreService = Depends(get_genre_service),
) -> list[DetailGenre] | None:
    genres = await service.get_multi(str(request.url.include_query_params()))
    if not genres:
        url = str(request.url.include_query_params())
        logger.debug(f'[-] {settings.genre_msg}. url:{url}')  # noqa: PIE803
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=settings.genre_msg)
    return genres
