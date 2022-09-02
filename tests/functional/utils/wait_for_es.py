import os

from backoff import backoff
from elasticsearch import Elasticsearch, TransportError


@backoff()
def check_connection(host: str = os.environ.get('ELASTIC_HOST')) -> bool:
    """
    Реализация отказоустойчивости, проверка связи с сервером Elasticsearch.
    :param host: URL.
    :return: bool.
    """
    es_client = Elasticsearch(host)
    if not es_client.ping():
        raise TransportError('Нет связи с сервером Elasticsearch')
    return es_client.ping()


if __name__ == '__main__':
    while True:
        if check_connection():
            break
