from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.users.schemas import UserRegisterSchema, UserLoginSchema
from app.users.dao import UserDAO
from app.users.auth import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from app.users.models import UserTable

from app.exceptions import UserAlreadyExistsException, IncorrectEmailException, IncorrectPasswordException

from app.users.dependencies import get_current_user


router = APIRouter(
    prefix='/auth',
    tags=['Auth Users']
)


@router.post(path='/register')
async def register_user(user_data: UserRegisterSchema):
    already_existing = await UserDAO.find_one_or_none(email=user_data.email)
    if already_existing:
        raise UserAlreadyExistsException()
    user_hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=user_hashed_password)
    return {'Status': 'User add!'}


@router.post(path='/login')
async def login_user(response: Response, user_data: UserLoginSchema):
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if not user:
        raise IncorrectEmailException()
    if not verify_password(user_data.password, user.hashed_password):
        raise IncorrectPasswordException()
    access_token = create_access_token({'sub': str(user.id)}, expires_delta=timedelta(minutes=15))
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return access_token


@router.post(path='/logout')
async def logout_user(response: Response) -> dict:
    response.delete_cookie('booking_access_token')
    return {'status': 'user logout!'}


@router.get(path='/me')
async def about_me(cur_user: UserTable = Depends(get_current_user)):
    return cur_user



