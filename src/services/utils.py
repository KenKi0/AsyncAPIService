from hashlib import md5


def create_key(params: str) -> str:
    """Получение хешированного ключа для Redis.

    Args:
            params: Параметры запроса к API.

        Returns:
            str: Список объектов модели Film | None.
    """

    return md5(params.encode()).hexdigest()  # noqa: DUO130
