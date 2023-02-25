import pytest
import pytest_asyncio
from alembic.command import upgrade
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from application.app import app
from application.db import get_session
from application.settings import db_settings


@pytest.fixture(scope="session", autouse=True)
def migrated_postgres(alembic_config):
    """
    Возвращает URL к БД с примененными миграциями.
    """
    upgrade(alembic_config, 'head')


async def _get_test_db():
    try:
        test_engine = create_async_engine(
            db_settings.get_async_pg_url(is_test=True), echo=True
        )

        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        pass


@pytest_asyncio.fixture(scope="function")
async def client():
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_session] = _get_test_db
    with TestClient(app) as test_client:
        yield test_client
