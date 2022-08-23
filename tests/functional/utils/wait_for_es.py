import time

from elasticsearch import Elasticsearch

if __name__ == '__main__':
    es_client = Elasticsearch({'host': 'elastic', 'port': '9200'})
    while True:
        if a := es_client.ping():
            break
        time.sleep(1)
