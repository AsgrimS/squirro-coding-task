from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.routers import documents

app = FastAPI()

app.include_router(documents.router, prefix="/documents", tags=["documents"])


@app.on_event("startup")
async def startup():
    FastAPICache.init(backend=InMemoryBackend(), prefix="fastapi-cache")


@app.get("/")
async def root():
    return {"message": "Visit /docs for API documentation"}
