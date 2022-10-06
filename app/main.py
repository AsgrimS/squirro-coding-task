from bson import ObjectId
from fastapi import Body, FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from motor import motor_asyncio
from pydantic import BaseModel, BaseSettings, Field


class Settings(BaseSettings):
    mongo_db: str
    mongo_username: str
    mongo_password: str

    class Config:
        env_file = ".env"


app = FastAPI()
settings = Settings()
print(settings.mongo_db, settings.mongo_username, settings.mongo_password)
client = motor_asyncio.AsyncIOMotorClient(
    f"mongodb://{settings.mongo_username}:{settings.mongo_password}@mongo:27017/{settings.mongo_db}"
)
db = client[settings.mongo_db]


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object id")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class DocumentBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class DocumentModel(DocumentBaseModel):
    content: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/documents/", response_description="Add new document", response_model=DocumentModel)
async def create_document(document: DocumentModel = Body(...)):
    document = jsonable_encoder(document)
    new_document = await db["documents"].insert_one(document)
    created_document = await db["documents"].find_one({"_id": new_document.inserted_id})
    return created_document


@app.get("/documents/", response_description="List all documents", response_model=list[DocumentBaseModel])
async def list_documents():
    documents = await db["documents"].find({}, {"title": 1}).to_list(None)
    return documents


@app.get("/documents/{doc_id}", response_description="Get a single document", response_model=DocumentModel)
async def get_document(doc_id: str):
    if (document := await db["documents"].find_one({"_id": doc_id})) is not None:
        return document

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Document {doc_id} not found")


@app.delete("/documents/{doc_id}", response_description="Delete a document", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(doc_id: str):
    results = await db["documents"].delete_one({"_id": doc_id})
    if results.deleted_count == 1:
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Document {doc_id} not found")
