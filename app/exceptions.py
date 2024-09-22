from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already registered!!!"


class IncorrectEmailException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'This email is not existing!'


class IncorrectPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Password is not correct!'


class IncorrectJWTException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token is not JWT format!'


class NoExpireTimeInCookiesException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'No exp in JWT cookies!'


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'JWT correct but expired!'


class NoSubjectInCookiesException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'No sub in JWT cookies!'


class UserNotFoundException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'User Not Found'
