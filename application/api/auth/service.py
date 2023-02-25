from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from application import schemes as sh

from .storage import add_user
from .http_exception import USER_ALREADY_EXIST


async def create_user(session: AsyncSession, user: sh.UserCreate):
    try:
        user = await add_user(session, user)
    except IntegrityError as exc:
        raise USER_ALREADY_EXIST
    return sh.UserShow.from_orm(user)
