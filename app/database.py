from fastapi import Depends
from motor import motor_asyncio

from app.settings import settings


async def get_db():
    client = motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{settings.mongo_username}:{settings.mongo_password}@mongo:27017/{settings.mongo_db}"
    )
    try:
        yield client[settings.mongo_db]
    finally:
        client.close()


async def get_documents_collection(db=Depends(get_db)):
    return db["documents"]
