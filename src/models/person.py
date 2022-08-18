from typing import Optional

from mixin import DefaultModel
from pydantic import BaseModel


class Person(BaseModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    full_name: str
    roles: Optional[list[str]]
    film_ids: Optional[list[str]]


class FilmPerson(DefaultModel):
    """Информация о персонах."""

    full_name: str


class DetailPerson(FilmPerson):
    """Полная информация по персонам."""

    role: Optional[list[str]]
    film_ids: Optional[list[str]]
