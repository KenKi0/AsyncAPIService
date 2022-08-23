import os
import time

from elasticsearch import Elasticsearch

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=os.environ.get('ELASTIC_HOST'))
    while True:
        if es_client.ping():
            break
        time.sleep(1)
