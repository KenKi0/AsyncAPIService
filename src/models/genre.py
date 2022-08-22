from typing import Optional

from models.utils import DefaultModel


class Genre(DefaultModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    name: str
    description: Optional[str]


class FilmGenre(DefaultModel):
    """Информация о жанре."""

    uuid: str
    name: str


class DetailGenre(FilmGenre):
    """Полная информация по жанрам."""

    description: Optional[str]
