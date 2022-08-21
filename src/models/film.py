from typing import Optional

from models.genre import FilmGenre
from models.person import FilmPerson
from models.utils import DefaultModel


class Film(DefaultModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    title: str
    description: Optional[str]
    imdb_rating: float
    director: Optional[list[dict]]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    actors: Optional[list[dict]]
    writers: Optional[list[dict]]
    genre: Optional[list[dict]]


class FilmResponse(DefaultModel):
    """Информация о фильме на главной странице | странице поиска."""

    uuid: str
    title: str
    imdb_rating: float


class DetailFilmResponse(FilmResponse):
    """Полная информация по фильму."""

    description: Optional[str] = ''
    genre: Optional[list[FilmGenre]]
    actors: Optional[list[FilmPerson]]
    writers: Optional[list[FilmPerson]] = []
    directors: Optional[list[FilmPerson]]
