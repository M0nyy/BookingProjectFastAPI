from fastapi import APIRouter, Path, status, Depends, HTTPException
from typing import Annotated
from app.users.dependencies import get_current_user

from app.bookings.schemas import BookingSchema
from app.users.models import UserTable

from app.bookings.dao import BookingDAO

from datetime import date

from pydantic import parse_obj_as

from fastapi_versioning import version

from app.tasks.tasks import send_booking_confirmation


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование'],
)


@router.get(path='', status_code=status.HTTP_200_OK)
@version(1)
async def get_bookings(user: UserTable = Depends(get_current_user)) -> list[BookingSchema]:
    return await BookingDAO.find_all(user_id=user.id)


@router.get(path='/{booking_id}')
@version(1)
async def get_booking_by_id(booking_id: Annotated[int, Path(..., ge=1)]) -> BookingSchema | None:
    result = await BookingDAO.find_by_id(booking_id)
    return result


@router.post(path='')
@version(1)
async def add_booking(room_id: int, date_from: date, date_to: date,
                      user: UserTable = Depends(get_current_user)):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)

    if not booking:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Не осталось свободных номеров')

    send_booking_confirmation.delay(user.email)

    return booking


@router.delete(path='/{booking_id}')
@version(1)
async def delete_booking(booking_id: int, user: UserTable = Depends(get_current_user)):
    booking = await BookingDAO.find_one_or_none(id=booking_id, user_id=user.id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Чужой аккаунт')
    await BookingDAO.delete(booking)
    return {"Answer": 'Успех'}


