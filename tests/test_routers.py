import pytest
from fastapi.encoders import jsonable_encoder

from app.models.documents import Document


@pytest.mark.anyio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Visit /docs for API documentation"}


@pytest.mark.anyio
async def test_get_documents(client, documents_collection):
    document = jsonable_encoder(Document(title="Test document", content="Test content"))
    new_document = await documents_collection.insert_one(document)

    response = await client.get("/documents/")

    assert response.status_code == 200
    assert response.json() == [{"_id": new_document.inserted_id, "title": document["title"]}]
