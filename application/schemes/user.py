import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class UserShow(BaseModel):
    name: str
    surname: str
    email: EmailStr
    user_uuid: uuid.UUID
    user_id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    name: str
    surname: str
    email: EmailStr
    user_uuid: uuid.UUID
    user_id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class UserFull(UserRead):
    password: str


class UserFromToken(BaseModel):
    user_id: int
    email: EmailStr
    user_uuid: uuid.UUID
    is_admin: bool
    is_active: bool = True

    class Config:
        orm_mode = True
