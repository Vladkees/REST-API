# app/__init__.py

from fastapi import FastAPI
from .routers import books  # Тут можеш імпортувати свої роутери

def create_app():
    app = FastAPI()
    app.include_router(books.router)  # Підключаємо маршрути для книги
    return app
