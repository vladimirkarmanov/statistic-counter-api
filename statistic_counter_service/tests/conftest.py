import asyncio
import logging
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app import app
from core.database import engine
from models.base import Base

logger = logging.getLogger("api")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client(event_loop: asyncio.AbstractEventLoop) -> AsyncGenerator[AsyncClient, None]:
    Base.metadata.create_all(bind=engine)
    async with AsyncClient(base_url="http://8000", app=app) as client:
        yield client
    Base.metadata.drop_all(bind=engine)


@pytest_asyncio.fixture(scope="function")
async def client_with_teardown(client):
    yield client


@pytest.fixture(scope="function")
def full_correct_statistic():
    yield {
        "date": "2023-03-12",
        "views": 100,
        "clicks": 50,
        "cost": 12.55
    }
