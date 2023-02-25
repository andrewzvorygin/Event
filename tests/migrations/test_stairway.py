"""
Stairway-тест не требует поддержки и позволяет быстро и дешево находить
огромное количество распространенных типовых ошибок в миграциях:
- не реализованные методы downgrade,
- не удаленные типы данных в методах downgrade (например, enum),
- опечатки и другие ошибки.
Идея теста заключается в том, чтобы накатывать миграции по одной,
последовательно выполняя для каждой миграции методы upgrade, downgrade,
upgrade.
Подробнее про stairway тест можно посмотреть в записи доклада с Moscow
Python: https://bit.ly/3bpJ0gw
"""
import uuid

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory

from sqlalchemy_utils import create_database, drop_database

from application.utils.pg import make_alembic_config
from application.settings import db_settings as db_set


def db_name():
    return '.'.join([uuid.uuid4().hex, 'pytest'])


def postgres():
    """
    Создает временную БД для запуска теста.
    """
    pg_url = db_set.get_psycopg_pg_url(is_test=True, db_name=db_name())
    create_database(pg_url)
    try:
        yield pg_url
    finally:
        drop_database(pg_url)


def alembic_config():
    """
    Создает объект с конфигурацией для alembic, настроенный на временную БД.
    """
    return make_alembic_config(next(postgres()))


def get_revisions():

    config = alembic_config()

    # Получаем директорию с миграциями alembic
    revisions_dir = ScriptDirectory.from_config(config)

    # Получаем миграции и сортируем в порядке от первой до последней
    revisions = list(revisions_dir.walk_revisions('base', 'heads'))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize('revision', get_revisions())
def test_migrations_stairway(alembic_config: Config, revision: Script):
    upgrade(alembic_config, revision.revision)
    # -1 используется для downgrade первой миграции (т.к. ее down_revision
    # равен None)
    downgrade(alembic_config, revision.down_revision or '-1')
    upgrade(alembic_config, revision.revision)
