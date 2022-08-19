from typing import Optional

from pydantic import BaseModel

from models.mixin import DefaultModel


class Genre(BaseModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    name: str
    description: Optional[str]


class DetailGenre(DefaultModel):
    """Полная информация по жанрам."""

    name: str
