from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:  # Хэшируем пароль
    return pwd_context.hash(password)


def verify_password(input_password: str, correct_password: str) -> bool:  # Сравниваем введенный пароль с паролем из БД
    return pwd_context.verify(input_password, correct_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


