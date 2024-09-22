from fastapi import APIRouter, status, Path, Query
from typing import Annotated
from app.hotels.dao import HotelsDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.schemas import HotelSchema
from app.hotels.rooms.schemas import RoomSchema
from datetime import date
from fastapi_cache.decorator import cache

from asyncio import sleep


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels']
)


@router.get(path='', status_code=status.HTTP_200_OK)
async def get_hotels() -> list[HotelSchema]:
    hotels = await HotelsDAO.find_all()
    return hotels


@router.get(path='/id/{hotel_id}',  status_code=status.HTTP_200_OK)
async def get_hotel_by_id(hotel_id: int) -> HotelSchema:
    hotel = await HotelsDAO.find_one_or_none(id=hotel_id)
    return hotel


@router.get(path='/{hotel_location}', status_code=status.HTTP_200_OK)
@cache(expire=20)
async def get_hotel_by_location(hotel_location: str | None = None):
    await sleep(3)
    hotel = await HotelsDAO.find_all(location=hotel_location)
    return hotel


@router.get(path='', status_code=status.HTTP_200_OK)
async def get_hotel_by_location_and_time(hotel_location: str | None = None,
                                         date_from: date = date.today(),
                                         date_to: date = date.today()):
    hotel = await HotelsDAO.find_all(location=hotel_location, date_from=date_from, date_to=date_to)
    return hotel


@router.get(path='/{hotel_id}/rooms/{room_id}', status_code=status.HTTP_200_OK)
async def get_hotel_room_by_id(hotel_id: int, room_id: int) -> RoomSchema:
    print(type(hotel_id), type(room_id))
    room = await RoomDAO.find_one_or_none(hotel_id=hotel_id, id=room_id)
    return room

