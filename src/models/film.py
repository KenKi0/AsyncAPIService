from typing import Optional

from pydantic.fields import Field

from models.genre import Genre
from models.person import Person
from models.utils import DefaultModel


class ESFilmPerson(DefaultModel):

    uuid: str = Field(..., alias='id')
    full_name: str = Field(..., alias='name')


class ESFilmGenre(DefaultModel):

    uuid: str = Field(..., alias='id')
    name: str


class ESFilm(DefaultModel):
    """Модель описывающая document в Elasticserch."""

    uuid: str = Field(..., alias='id')  # noqa: VNE003
    title: str
    description: Optional[str]
    imdb_rating: float
    director: Optional[list[ESFilmPerson]]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    actors: Optional[list[ESFilmPerson]]
    writers: Optional[list[ESFilmPerson]]
    genre: Optional[list[ESFilmGenre]]


class FilmResponse(DefaultModel):
    """Информация о фильме на главной странице | странице поиска."""

    uuid: str
    title: str
    imdb_rating: float


class DetailFilmResponse(FilmResponse):
    """Полная информация по фильму."""

    description: Optional[str] = ''
    genre: Optional[list[Genre]]
    actors: Optional[list[Person]]
    writers: Optional[list[Person]] = []
    directors: Optional[list[Person]]
