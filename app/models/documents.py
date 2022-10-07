from bson import ObjectId
from pydantic import BaseModel, Field


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


class DocumentBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class Document(DocumentBase):
    content: str


class DocumentInput(Document):
    class Config:
        schema_extra = {
            "example": {
                "title": "Document title",
                "content": "Document content",
            }
        }
