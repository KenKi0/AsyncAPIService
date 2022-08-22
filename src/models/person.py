from typing import Optional

from models.utils import DefaultModel


class Person(DefaultModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    full_name: str
    role: Optional[list[str]]
    film_ids: Optional[list[str]]


class FilmPerson(DefaultModel):
    """Информация о персонах."""

    uuid: str
    full_name: str


class DetailPerson(FilmPerson):
    """Полная информация по персонам."""

    role: Optional[list[str]]
    film_ids: Optional[list[str]]
