from typing import Optional

from pydantic import BaseModel

from models.utils import DefaultModel


class Genre(BaseModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    name: str
    description: Optional[str]


class FilmGenre(DefaultModel):
    """Информация о жанре."""

    name: str


class DetailGenre(FilmGenre):
    """Полная информация по жанрам."""

    description: Optional[str]
