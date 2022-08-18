from typing import Optional

from mixin import DefaultModel
from pydantic import BaseModel


class Genre(BaseModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    name: str
    description: Optional[str]


class DetailGenre(DefaultModel):
    """Полная информация по жанрам."""

    name: str
