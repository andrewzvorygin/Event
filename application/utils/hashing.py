from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30   # Действие токена - 30 минут
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 60   # Действие токена - 60 дней


def get_password_hash(password) -> str:
    """Получить хэшированный пароль"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Проверить пароль пользователя"""
    return pwd_context.verify(plain_password, hashed_password)
