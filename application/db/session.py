from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from application.settings import db_settings as db_set


engine = create_async_engine(
    db_set.get_async_pg_url(), echo=True,
)

# create session for the interaction with database
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> Generator:
    """Зависимость для получения асинхронной сессии"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
