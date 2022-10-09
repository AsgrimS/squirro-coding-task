from fastapi import Depends, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi_cache.decorator import cache

from app.database import get_documents_collection
from app.models.documents import Document, DocumentBase, DocumentInput, DocumentSummary
from app.settings import settings
from app.summarize import get_summarization

router = APIRouter()


class DocumentNotFoundException(HTTPException):
    def __init__(self, document_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id '{document_id}' not found",
        )


@router.post("/", description="Add a new document.", response_model=DocumentBase, status_code=status.HTTP_201_CREATED)
async def create_document(document: DocumentInput, documents_collection=Depends(get_documents_collection)):
    document = jsonable_encoder(document)
    new_document = await documents_collection.insert_one(document)
    created_document = await documents_collection.find_one({"_id": new_document.inserted_id}, {"content": 0})
    return created_document


@router.get("/", description="List all documents titles and ids.", response_model=list[DocumentBase])
async def list_documents(documents_collection=Depends(get_documents_collection)):
    documents = await documents_collection.find({}, {"title": 1}).to_list(None)
    return documents


@router.get("/{doc_id}", description="Get a single document by id.", response_model=Document)
async def get_document(doc_id: str, documents_collection=Depends(get_documents_collection)):
    if (document := await documents_collection.find_one({"_id": doc_id})) is not None:
        return document

    raise DocumentNotFoundException(doc_id)


@router.delete("/{doc_id}", description="Delete a single document by id.", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(doc_id: str, documents_collection=Depends(get_documents_collection)):
    results = await documents_collection.delete_one({"_id": doc_id})
    if results.deleted_count == 1:
        return

    raise DocumentNotFoundException(doc_id)


@router.get(
    "/summarize/{doc_id}",
    description="Summarize a single document by id. Cached for 10 minutes.",
    response_model=DocumentSummary,
)
@cache(expire=settings.summarization_cache_timeout)
async def summarize_document(
    doc_id: str,
    summary_percentage: float = Query(
        description="Size of the summary compared to the article in %.", gt=0, le=1, default=0.05
    ),
    documents_collection=Depends(get_documents_collection),
):
    if (document := await documents_collection.find_one({"_id": doc_id})) is None:
        raise DocumentNotFoundException(doc_id)

    return {"_id": document["_id"], "summary": get_summarization(document["content"], summary_percentage)}
