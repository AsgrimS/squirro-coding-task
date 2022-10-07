from fastapi import FastAPI

from app.routers import documents

app = FastAPI()

app.include_router(documents.router, prefix="/documents", tags=["documents"])


@app.get("/")
async def root():
    return {"message": "Visit /docs for API documentation"}
