"""Модуль для описания ошибок"""
from fastapi import HTTPException
from starlette import status


USER_ALREADY_EXIST = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail='Пользователь с таким email уже существует'
)

INCORRECT_LOGIN_OR_PASSWORD_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный логин или пароль"
)

CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидный токен"
)