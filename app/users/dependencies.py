from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from app.settings import settings
from datetime import datetime, timezone
from app.users.dao import UserDAO
from app.users.models import UserTable

from app.exceptions import IncorrectJWTException, NoExpireTimeInCookiesException, TokenExpiredException, NoSubjectInCookiesException, UserNotFoundException


def get_token(request: Request):
    token = request.cookies.get('booking_access_token', None)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise IncorrectJWTException()

    expire_time: str = payload.get('exp')
    if not expire_time:
        raise NoExpireTimeInCookiesException()

    if expire_time < int(datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException()

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoSubjectInCookiesException()

    user: UserTable = await UserDAO.find_by_id(int(user_id))

    if not user:
        raise UserNotFoundException()

    return user

