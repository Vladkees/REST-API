from fastapi import FastAPI, HTTPException
from .schemas import Book
from .storage import books

app = FastAPI()

@app.get("/books")
async def get_books():
    return books

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", status_code=201)
async def add_book(book: Book):
    if any(b["id"] == book.id for b in books):
        raise HTTPException(status_code=400, detail="Book with this ID already exists")
    books.append(book.dict())
    return book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    books = [b for b in books if b["id"] != book_id]
    return {"message": "Book deleted"}
