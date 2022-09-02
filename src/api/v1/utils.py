from enum import Enum

from fastapi import Query
from pydantic import BaseConfig


class SortEnum(str, Enum):
    desc_rating = '-imdb_rating'
    asc_rating = 'imdb_rating'


class PaginatedParams(BaseConfig):
    PAGE_NUM: int = Query(default=1, alias='page[number]', ge=1)
    PAGE_SIZE: int = Query(default=50, alias='page[size]', ge=1)


pagination = PaginatedParams()
