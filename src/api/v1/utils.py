from enum import Enum


class SortEnum(str, Enum):
    desc_rating = '-imdb_rating'
    asc_rating = 'imdb_rating'
