from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class RedisSettings(BaseConfig):
    HOST: str = '127.0.0.1'
    PORT: int = 6379

    class Config:
        env_prefix = 'REDIS_'

    @property
    def url(self):
        return f'redis://{self.HOST}:{self.PORT}'


class ElasticSettings(BaseConfig):
    HOST: str = '127.0.0.1'
    PORT: int = 9200

    class Config:
        env_prefix = 'ES_'

    @property
    def hosts(self):
        return [{'host': self.HOST, 'port': self.PORT}]


class ProjectSettings(BaseConfig):

    PROJECT_NAME: str = 'movies'
    BASE_DIR = Path(__file__).parent.parent
    redis: RedisSettings = RedisSettings()
    elastic: ElasticSettings = ElasticSettings()


settings = ProjectSettings()
