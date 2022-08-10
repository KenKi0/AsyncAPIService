from typing import Optional

from pydantic import BaseModel

from .genre import DetailGenre
from .mixin import BaseModelMixin
from .person import PersonFilm


class Film(BaseModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    title: str
    description: Optional[str]
    imdb_rating: Optional[float]
    director: Optional[list[str]]
    actors: Optional[list[dict]]
    writers: Optional[list[dict]]
    genre: Optional[list[str]]


class FilmResponse(BaseModelMixin):
    """Информация о фильме на главной странице | странице поиска.

    Requests:
        - /api/v1/films/
        - /api/v1/films?sort=.../
        - /api/v1/films/search/
        - /api/v1/persons/<uuid:UUID>/film/
    """

    title: str
    imdb_rating: Optional[float]


class DetailFilmResponse(FilmResponse):
    """Полная информация по фильму.

    Requests:
        - /api/v1/films/<uuid:UUID>/
    """

    description: Optional[str]
    genre: Optional[list[DetailGenre]]
    actors: Optional[list[PersonFilm]]
    writers: Optional[list[PersonFilm]]
    directors: Optional[list[PersonFilm]]
