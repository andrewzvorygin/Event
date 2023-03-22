from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .service import create_user

from application import schemes as sh
from application.db import get_session

auth_router = APIRouter()


@auth_router.post('/registration', response_model=sh.UserShow, status_code=status.HTTP_201_CREATED)
async def registration(data: sh.UserCreate, session: AsyncSession = Depends(get_session)):
    """Регистрация пользователя"""
    return await create_user(session, data)

