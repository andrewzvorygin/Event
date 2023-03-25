from fastapi import APIRouter, Depends, status, Response

from sqlalchemy.ext.asyncio import AsyncSession

from . import service

from application import schemes as sh
from application.db import get_session

auth_router = APIRouter()


@auth_router.post('/registration', response_model=sh.UserShow, status_code=status.HTTP_201_CREATED)
async def registration(data: sh.UserCreate, session: AsyncSession = Depends(get_session)):
    """Регистрация пользователя"""
    return await service.create_user(session, data)


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(response: Response, data: sh.UserLogin, session: AsyncSession = Depends(get_session)):
    """Регистрация пользователя"""
    user = await service.authenticate_user(session, data)
    authorization_token: sh.RefreshSession = await service.get_authorization_token(session, user)
    response.set_cookie(
        key='refresh_token',
        value=str(authorization_token.refresh_session),
        httponly=True,
        max_age=authorization_token.expires_in
    )
    return {'access_token': authorization_token.access_token}


@auth_router.get("/isAuth", status_code=status.HTTP_200_OK)
async def is_auth(current_user: sh.UserFromToken = Depends(service.get_current_user)):
    return {'user_id': current_user.user_id}
