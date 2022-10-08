import pytest
from httpx import AsyncClient
from motor import motor_asyncio

from app.database import get_db
from app.main import app

TEST_DB_NAME = "squirrodb_test"
TEST_DB_URL = f"mongodb://test:test123@mongo_test:27017/{TEST_DB_NAME}"


async def db_override():
    client = motor_asyncio.AsyncIOMotorClient(TEST_DB_URL)
    try:
        yield client[TEST_DB_NAME]
    finally:
        client.close()


app.dependency_overrides[get_db] = db_override


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def db():
    client = motor_asyncio.AsyncIOMotorClient(TEST_DB_URL)
    try:
        db = client[TEST_DB_NAME]
        [await db[collection].drop() for collection in await db.list_collection_names()]
        yield db
    finally:
        client.close()


@pytest.fixture
async def documents_collection(db):
    return db["documents"]
