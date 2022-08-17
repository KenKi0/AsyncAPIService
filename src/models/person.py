from typing import Optional

from pydantic import BaseModel

from .mixin import BaseModelMixin


class Person(BaseModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    full_name: str
    roles: Optional[list[str]]
    film_ids: Optional[list[str]]


class FilmPerson(BaseModelMixin):
    """Информация о персонах."""

    full_name: str


class DetailPerson(FilmPerson):
    """Полная информация по персонам."""

    role: Optional[list[str]]
    film_ids: Optional[list[str]]
