import dataclasses
from enum import Enum
from datetime import datetime

from fastapi import Query, Request, HTTPException
from fastapi.security import HTTPBearer
import jwt

from core.config import settings


class SortEnum(str, Enum):
    desc_rating = '-imdb_rating'
    asc_rating = 'imdb_rating'


@dataclasses.dataclass
class PaginatedParams:
    num: int = 1
    size: int = 50

    def __init__(
        self,
        num: int = Query(default=1, alias='page[number]', ge=1),
        size: int = Query(default=50, alias='page[size]', ge=1),
    ):
        self.num = num
        self.size = size


def get_verified_jwt(jwtoken: str) -> dict:
    decoded_token = jwt.decode(jwtoken, settings.jwt.SECRET_KEY, algorithms=[settings.jwt.ALGORITHM])
    return decoded_token if decoded_token['exp'] >= datetime.now() else None


async def get_permissions(request: Request) -> list:
    """
    Возвращает разрешения пользователя
    :param request: запрос, передаётся автоматически при использовании Depends в ручке
    :return: список разрешений
    """
    try:
        bearer = HTTPBearer()
        credentials = await bearer(request)
        claims = get_verified_jwt(credentials.credentials)
        return claims.get('permissions') if claims.get('permissions') else []
    except HTTPException as e:
        return []
