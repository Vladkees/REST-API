from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Створюємо Flask додаток
app = Flask(__name__)

# Налаштовуємо з'єднання з базою даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/library_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для таблиці книг
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)

# Головна сторінка
@app.route('/')
def index():
    return "Welcome to the library API!"

# Отримання всіх книг з пагінацією (GET)
@app.route('/books', methods=['GET'])
def get_books():
    limit = request.args.get('limit', default=10, type=int)  # Обмеження
    offset = request.args.get('offset', default=0, type=int)  # Відступ
    books = Book.query.offset(offset).limit(limit).all()
    
    result = []
    for book in books:
        result.append({
            'id': book.id,
            'title': book.title,
            'author': book.author
        })
    
    return jsonify(result)

# Додавання нової книги (POST)
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({
        'id': new_book.id,
        'title': new_book.title,
        'author': new_book.author
    }), 201

# Видалення книги (DELETE)
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({'message': 'Book deleted'}), 200

if __name__ == '__main__':
    # Запуск сервера на порту 5000
    app.run(host='0.0.0.0', port=5000)
