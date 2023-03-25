from datetime import timedelta, datetime

from fastapi import Header
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from application import schemes as sh

from . import storage as st

from .http_exception import USER_ALREADY_EXIST, INCORRECT_LOGIN_OR_PASSWORD_EXCEPTION, CREDENTIALS_EXCEPTION
from application.utils.hashing import get_password_hash, verify_password
from application.utils.hashing import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, REFRESH_TOKEN_EXPIRE_MINUTES

from application.settings import api_settings


async def create_user(session: AsyncSession, user: sh.UserCreate) -> sh.UserShow:
    try:
        user.password = get_password_hash(user.password)
        user = await st.add_user(session, user)
    except IntegrityError:
        raise USER_ALREADY_EXIST
    return sh.UserShow.from_orm(user)


async def authenticate_user(session: AsyncSession, user_login: sh.UserLogin) -> sh.UserFull:
    """Аутентификация пользователя"""
    user_model = await st.get_user_by_email(session=session, email=user_login.email)
    if user_model is None:
        raise INCORRECT_LOGIN_OR_PASSWORD_EXCEPTION
    user = sh.UserFull.from_orm(user_model)
    if not verify_password(user_login.password, user.password):
        raise INCORRECT_LOGIN_OR_PASSWORD_EXCEPTION
    return user


async def get_authorization_token(session: AsyncSession, user: sh.UserFull) -> sh.RefreshSession:
    """Получить токен авторизации"""
    access_token = await get_access_token(user)
    refresh_session = sh.RefreshSession(
        user_id=user.user_id,
        access_token=access_token,
        expires_in=REFRESH_TOKEN_EXPIRE_MINUTES,
        time_created=datetime.utcnow()
    )
    await st.add_refresh_session(session, refresh_session)
    return refresh_session


async def get_access_token(user: sh.UserFull) -> str:
    return await get_token(user, ACCESS_TOKEN_EXPIRE_MINUTES)


async def get_token(user: sh.UserFull, time_expires: int) -> str:
    token_expires = timedelta(minutes=time_expires)
    data_to_token = dict(
        user_id=user.user_id,
        email=user.email,
        user_uuid=str(user.user_uuid),
        is_admin=user.is_admin,
        is_active=user.is_active
    )
    token = create_token(
        data=data_to_token, expires_delta=token_expires
    )
    return token


def create_token(data: dict, expires_delta: timedelta) -> str:
    """Создать токен"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, api_settings.secret_key_solt, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(access_token: str = Header()) -> sh.UserFromToken:
    """Получить текущего пользователя"""
    try:
        payload = jwt.decode(access_token, api_settings.secret_key_solt, algorithms=[ALGORITHM])
        user = sh.UserFromToken(**payload)
    except (JWTError, ValidationError):
        raise CREDENTIALS_EXCEPTION
    return user
