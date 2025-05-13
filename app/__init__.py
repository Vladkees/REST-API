from flask import Flask
from app.models import db
from app.routes import get_books

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Ініціалізуємо SQLAlchemy
    db.init_app(app)

    # Роут для отримання книг
    app.add_url_rule('/books', 'get_books', get_books)

    return app
