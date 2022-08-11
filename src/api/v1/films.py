from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.film import DetailFilmResponse, FilmResponse
from models.genre import DetailGenre
from models.person import FilmPerson
from src.services.film import FilmService, get_film_service

router = APIRouter()


# Параметры для запроса:
# sort
# page[size] # noqa: E800
# page[number] # noqa: E800
# filter[genre] # noqa: E800
@router.get('/', response_model=FilmResponse)
async def film_response(*params, film_service: FilmService = Depends(get_film_service)) -> FilmResponse:
    """Главная страница с фильмами.

    Args:
            *params: .... !!!надо определиться с ними!!!
            film_service: Провайдер для FilmService.

    Returns:
            FilmResponse: Объект модели FilmResponse.
    """

    return


# Параметры для запроса:
# sort ??
# page[size] # noqa: E800
# page[number] # noqa: E800
# query
@router.get('/search', response_model=FilmResponse)
async def search_film_response(*params, film_service: FilmService = Depends(get_film_service)) -> FilmResponse:
    """Поиск по фильмам.

    Args:
            *params: .... !!!надо определиться с ними!!!
            film_service: Провайдер для FilmService.

    Returns:
            FilmResponse: Объект модели FilmResponse.
    """

    return


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
    genre_list = [DetailGenre(uuid=item.get('uuid'), name=item.get('name')) for item in film.genre]
    actors_list = [FilmPerson(uuid=item.get('uuid'), full_name=item.get('full_name')) for item in film.actors]
    writers_list = [FilmPerson(uuid=item.get('uuid'), full_name=item.get('full_name')) for item in film.writers]
    directors_list = [FilmPerson(uuid=item.get('uuid'), full_name=item.get('full_name')) for item in film.directors]
    return DetailFilmResponse(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=genre_list,
        actors=actors_list,
        writers=writers_list,
        directors=directors_list,
    )
