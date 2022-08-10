from pydantic import BaseModel

from .mixin import BaseModelMixin


class Genre(BaseModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    name: str


class DetailGenre(BaseModelMixin):
    """Полная информация по жанрам.

    Requests:
        - /api/v1/genres/
        - /api/v1/genres/<uuid:UUID>/
        - /api/v1/films/<uuid:UUID>/
    """

    name: str
