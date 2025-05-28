from app.db import collection
from app.models import Book

from pydantic_mongo import PydanticObjectId

async def create_book(book: Book):
    result = await collection.insert_one(book.dict(by_alias=True, exclude_none=True))
    return str(result.inserted_id)

async def get_book(book_id: str):
    from bson import ObjectId
    return await collection.find_one({"_id": ObjectId(book_id)})

async def get_all_books():
    books = []
    async for book in collection.find({}):
        books.append(Book(**book))
    return books

async def delete_book(book_id: str):
    from bson import ObjectId
    result = await collection.delete_one({"_id": ObjectId(book_id)})
    return result.deleted_count
