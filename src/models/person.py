from typing import Optional

from pydantic import BaseModel

from .mixin import BaseModelMixin


class Person(BaseModel):
    """Модель описывающая document в Elasticserch."""

    id: str  # noqa: VNE003
    full_name: str
    roles: Optional[list]
    film_ids: Optional[list]


class FilmPerson(BaseModelMixin):
    """Информация о персонах.

    Requests:
        - /api/v1/films/<uuid:UUID>/
    """

    full_name: str


class DetailPerson(FilmPerson):
    """Полная информация по персонам.

    Requests:
        - /api/v1/persons/<uuid:UUID>/
        - /api/v1/persons/search/
    """

    role: str
    film_ids: Optional[list]
