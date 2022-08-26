from typing import Optional

from pydantic.fields import Field

from models.utils import DefaultModel


class ESGenre(DefaultModel):
    """Модель описывающая document в Elasticserch."""

    uuid: str = Field(..., alias='id')  # noqa: VNE003
    name: str
    description: Optional[str]


class Genre(DefaultModel):
    """Информация о жанре."""

    uuid: str
    name: str


class DetailGenre(Genre):
    """Полная информация по жанрам."""

    description: Optional[str]
