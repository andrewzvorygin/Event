"""Модуль для описания ошибок"""
from fastapi import HTTPException
from starlette import status


USER_ALREADY_EXIST = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail='Пользователь с таким email уже существует'
)
