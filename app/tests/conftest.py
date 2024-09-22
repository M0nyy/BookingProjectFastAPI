import json
import asyncio
import pytest
from app.database import Base, async_session_maker, engine
from app.settings import settings
from datetime import datetime

from app.main import app as fastapi_app

from app.bookings.models import BookingsTable
from app.users.models import UserTable
from app.hotels.rooms.models import RoomTable
from app.hotels.models import HotelTable

from sqlalchemy import insert

from fastapi.testclient import TestClient
from httpx import AsyncClient


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'app/tests/mock_{model}.json') as file:
            return json.load(file)

    hotels = open_mock_json('hotels')
    rooms = open_mock_json('rooms')
    users = open_mock_json('users')
    bookings = open_mock_json('bookings')

    for booking in bookings:
        booking['date_from'] = datetime.strptime(booking['date_from'], '%Y-%m-%d')
        booking['date_to'] = datetime.strptime(booking['date_to'], '%Y-%m-%d')

    async with async_session_maker() as session:
        add_hotels = insert(HotelTable).values(hotels)
        add_rooms = insert(RoomTable).values(rooms)
        add_users = insert(UserTable).values(users)
        add_bookings = insert(BookingsTable).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='function')
async def async_session():
    async with async_session_maker() as session:
        yield session