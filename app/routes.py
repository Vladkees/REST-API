from flask import request, jsonify
from app.models import db, Book
from math import ceil

# Отримання всіх книг з пагінацією
def get_books():
    try:
        # Отримуємо параметри пагінації
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Отримуємо книги з пагінацією
        books = Book.query.paginate(page, per_page, False)
        
        # Підготовка результатів
        result = {
            "total": books.total,
            "pages": books.pages,
            "current_page": books.page,
            "books": [
                {"id": book.id, "title": book.title, "author": book.author, "year": book.year}
                for book in books.items
            ]
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
