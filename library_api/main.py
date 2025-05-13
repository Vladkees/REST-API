from fastapi import FastAPI
from app.routers import books
from app.database import engine, Base

# Створити таблиці
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books.router)
