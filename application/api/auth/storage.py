from sqlalchemy.ext.asyncio import AsyncSession

from application.db.models import User

from application import schemes as sh


async def add_user(session: AsyncSession, user: sh.UserCreate) -> User:
    async with session.begin():
        new_user = User(**user.dict())
        session.add(new_user)
    return new_user
