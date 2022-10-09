import pytest
from fastapi.encoders import jsonable_encoder

from app.models.documents import Document


@pytest.mark.anyio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Visit /docs for API documentation"}


@pytest.mark.anyio
async def test_list_documents(client, documents_collection):
    document = jsonable_encoder(Document(title="Test document", content="Test content"))
    new_document = await documents_collection.insert_one(document)

    response = await client.get("/documents/")

    assert response.status_code == 200
    assert response.json() == [{"_id": new_document.inserted_id, "title": document["title"]}]


@pytest.mark.anyio
async def test_create_document(client, documents_collection):
    request_body = {"title": "Test document", "content": "Test content"}
    response = await client.post("/documents/", json=request_body)

    assert await documents_collection.count_documents({}) == 1

    assert response.status_code == 201
    assert response.json() == {"_id": response.json()["_id"], "title": request_body["title"]}


@pytest.mark.anyio
@pytest.mark.parametrize("request_body", [({"title": "Test document"}), ({"content": "Test content"}), ({})])
async def test_create_document_validation_error(request_body, client, documents_collection):
    response = await client.post("/documents/", json=request_body)

    assert await documents_collection.count_documents({}) == 0
    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_document(client, documents_collection):
    document = jsonable_encoder(Document(title="Test document", content="Test content"))
    new_document = await documents_collection.insert_one(document)

    response = await client.get(f"/documents/{new_document.inserted_id}")

    assert response.status_code == 200
    assert response.json() == {
        "_id": new_document.inserted_id,
        "title": document["title"],
        "content": document["content"],
    }


@pytest.mark.anyio
async def test_get_document_not_found(client):
    random_id = "foobar"
    response = await client.get(f"/documents/{random_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Document with id '{random_id}' not found"}


@pytest.mark.anyio
async def test_delete_document(client, documents_collection):
    document = jsonable_encoder(Document(title="Test document", content="Test content"))
    new_document = await documents_collection.insert_one(document)

    response = await client.delete(f"/documents/{new_document.inserted_id}")

    assert await documents_collection.count_documents({}) == 0
    assert response.status_code == 204


@pytest.mark.anyio
async def test_delete_document_not_found(client):
    random_id = "foobar"
    response = await client.delete(f"/documents/{random_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Document with id '{random_id}' not found"}


@pytest.mark.anyio
async def test_summarize_document(client, documents_collection):
    document = jsonable_encoder(Document(title="Test document", content="Test content"))
    new_document = await documents_collection.insert_one(document)

    response = await client.get(f"/documents/summarize/{new_document.inserted_id}", params={"summary_percentage": 1})

    assert response.status_code == 200
    assert response.json() == {"summary": "Test content"}


@pytest.mark.anyio
@pytest.mark.parametrize("query_params", [({"summary_percentage": 0}), ({"summary_percentage": 1.1})])
async def test_summarize_document_validation_error(query_params, client, documents_collection):
    document = jsonable_encoder(Document(title="Test document", content="Test content"))
    new_document = await documents_collection.insert_one(document)

    response = await client.get(f"/documents/summarize/{new_document.inserted_id}", params=query_params)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_summarize_document_not_found(client):
    random_id = "foobar"
    response = await client.get(f"/documents/summarize/{random_id}?summary_percentage=1")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Document with id '{random_id}' not found"}
