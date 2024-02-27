import pytest
from app.database import Base, async_session_maker, engine
from app.config import settings
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.Users.models import Users
import json
import asyncio
from sqlalchemy import insert
from datetime import datetime
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app as fastapi_app

@pytest.fixture(autouse=True, scope='session')
async def prepare_datadase():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
       await conn.run_sync(Base.metadata.drop_all)
       await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)
    
    
    hotels = open_mock_json('hotels')
    rooms = open_mock_json('rooms')
    users = open_mock_json('users')
    bookings = open_mock_json('bookings')

    for booking in bookings:
        booking['date_from'] = datetime.strptime(booking['date_from'], "%Y-%m-%d")
        booking['date_to'] = datetime.strptime(booking['date_to'], "%Y-%m-%d")


    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def ac():
    "Асинхронный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def autontificated_ac():
    "Асинхронный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post('/auth/login', json={
            "email": "test@test.com",
            "password": "test"
        })
        assert ac.cookies["bookings_access_token"]
        yield ac

""" @pytest.fixture(scope='function')
async def session():
    async with async_session_maker() as session:
        yield session
 """