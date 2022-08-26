from typing import Optional

from pydantic.fields import Field

from models.utils import DefaultModel


class ESPerson(DefaultModel):
    """Модель описывающая document в Elasticserch."""

    uuid: str = Field(..., alias='id')  # noqa: VNE003
    full_name: str
    role: Optional[list[str]]
    film_ids: Optional[list[str]]


class Person(DefaultModel):
    """Информация о персонах."""

    uuid: str
    full_name: str


class DetailPerson(Person):
    """Полная информация по персонам."""

    role: Optional[list[str]]
    film_ids: Optional[list[str]]
