from fastapi import FastAPI, HTTPException
from .models import Book
from app.crud import create_book, get_book, get_all_books, delete_book


app = FastAPI()

@app.post("/books", response_model=str)
async def add_book(book: Book):
    return await create_book(book)

@app.get("/books")
async def list_books():
    return await get_all_books()

@app.get("/books/{book_id}")
async def read_book(book_id: str):
    book = await get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}")
async def remove_book(book_id: str):
    deleted = await delete_book(book_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}
