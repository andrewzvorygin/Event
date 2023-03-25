import os
from pathlib import Path

from pydantic import BaseSettings


ROOT_PATH = Path(__file__).parent.parent
PATH_TO_ENV = os.path.join(ROOT_PATH, '.env')


class SettingsAPI(BaseSettings):
    host: str = 'localhost'
    port: int = 80
    secret_key_solt: str
    secret_key: str

    class Config:
        env_prefix = 'api_'
        env_file = PATH_TO_ENV


class SettingsDB(BaseSettings):
    host: str
    port: int
    name: str
    user: str
    password: str

    class Config:
        env_prefix = 'db_'
        env_file = PATH_TO_ENV

    @staticmethod
    def _get_url(*args, user, password, host, port, db_name, driver, is_test=False):
        return f'postgresql+{driver}://{user}:{password}@{host}:{port}/{db_name}{".pytest" if is_test else ""}'

    @staticmethod
    def _get_url_without_driver(*args, user, password, host, port, db_name, is_test=False):
        return f'postgresql://{user}:{password}@{host}:{port}/{db_name}{".pytest" if is_test else ""}'

    def get_async_pg_url(self, user=None, password=None, host=None, port=None, db_name=None, is_test=False):
        return self._get_url(
            driver='asyncpg',
            user=user or self.user,
            host=host or self.host,
            port=port or self.port,
            db_name=db_name or self.name,
            is_test=is_test,
            password=password or self.password
        )

    def get_psycopg_pg_url(self, user=None, password=None, host=None, port=None, db_name=None, is_test=False):
        return self._get_url(
            driver='psycopg2',
            is_test=is_test,
            user=user or self.user,
            host=host or self.host,
            port=port or self.port,
            db_name=db_name or self.name,
            password=password or self.password
        )

    def get_url_without_driver(self, user=None, password=None, host=None, port=None, db_name=None, is_test=False):
        return self._get_url_without_driver(
            is_test=is_test,
            user=user or self.user,
            host=host or self.host,
            port=port or self.port,
            db_name=db_name or self.name,
            password=password or self.password
        )


api_settings = SettingsAPI()
db_settings = SettingsDB()
