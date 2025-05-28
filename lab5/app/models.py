from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField

class Book(BaseModel):
    id: ObjectIdField = Field(default=None, alias="_id")
    title: str
    author: str
    year: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
