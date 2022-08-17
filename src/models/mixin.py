import orjson
from pydantic import BaseModel


def orjson_dumps(value, *, default):
    return orjson.dumps(value, default=default).decode()


class BaseModelMixin(BaseModel):
    """Mixin."""

    uuid: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps