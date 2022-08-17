from typing import Optional

from pydantic import BaseModel

from .mixin import BaseModelMixin


class Genre(BaseModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    name: str
    description: Optional[str]


class DetailGenre(BaseModelMixin):
    """Полная информация по жанрам."""

    name: str
