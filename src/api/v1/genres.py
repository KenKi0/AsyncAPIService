from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from models.genre import DetailGenre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/{uuid}', response_model=DetailGenre)
async def get_genre(
    uuid: str,
    request: Request,
    service: GenreService = Depends(get_genre_service),
):
    genre = service.get(uuid, str(request.url.include_query_params()))
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre with specified uuid not exists')
    return genre


@router.get('/', response_model=list[DetailGenre])
async def get_genres(
    request: Request,
    service: GenreService = Depends(get_genre_service),
):
    genres = service.get_multi(str(request.url.include_query_params()))
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre with specified uuid not exists')
    return genres
