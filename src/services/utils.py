from hashlib import md5


def create_key(params: str) -> str:
    """Получение хешированного ключа для Redis.

    Args:
        params: Параметры запроса к API.

    Returns:
        str: Хешированный ключ для Redis.
    """

    return md5(params.encode()).hexdigest()  # noqa: DUO130
