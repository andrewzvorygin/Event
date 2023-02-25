import uuid

import pytest
from sqlalchemy_utils import create_database, drop_database

from application.utils.pg import make_alembic_config
from application.settings import db_settings as db_set


# @pytest.fixture(scope="session")
# def db_name():
#     return '.'.join([uuid.uuid4().hex, 'pytest'])


@pytest.fixture(scope="session", autouse=True)
def postgres():
    """
    Создает временную БД для запуска теста.
    """
    pg_url = db_set.get_psycopg_pg_url(is_test=True)
    create_database(pg_url)
    try:
        yield pg_url
    finally:
        drop_database(pg_url)


@pytest.fixture(scope="session", autouse=True)
def alembic_config(postgres):
    """
    Создает объект с конфигурацией для alembic, настроенный на временную БД.
    """
    return make_alembic_config(postgres)
