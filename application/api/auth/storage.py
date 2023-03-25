from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete

from application.db.models import User, user_orm, refresh_session_orm

from application import schemes as sh


async def add_user(session: AsyncSession, user: sh.UserCreate) -> User:
    async with session.begin():
        new_user = User(**user.dict())
        session.add(new_user)
    return new_user


async def get_user_by_email(*args, session: AsyncSession, email: str):
    smtp = select(user_orm).where(user_orm.c.email == email)
    result = await session.execute(smtp)
    return result.fetchone()


async def add_refresh_session(session: AsyncSession, refresh_session: sh.RefreshSession) -> None:
    smtp = (
        insert(refresh_session_orm)
        .values(
            user_id=refresh_session.user_id,
            refresh_session=refresh_session.refresh_session,
            expires_in=refresh_session.expires_in,
            time_created=refresh_session.time_created
        )
    )
    await session.execute(smtp)
    await session.commit()
