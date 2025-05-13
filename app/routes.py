from flask import Blueprint, request, jsonify
from app.models import db, Book

bp = Blueprint('books', __name__)

# GET all books with pagination
@bp.route('/books', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    books = Book.query.paginate(page, per_page, error_out=False)
    
    return jsonify({
        'books': [{
            'id': book.id,
            'title': book.title,
            'author': book.author
        } for book in books.items],
        'total': books.total,
        'pages': books.pages,
        'current_page': books.page
    })
# GET a single book by ID
@bp.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author
    })

# POST a new book
@bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    
    if 'title' not in data or 'author' not in data:
        return jsonify({'error': 'Title and Author are required'}), 400
    
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        'id': new_book.id,
        'title': new_book.title,
        'author': new_book.author
    }), 201

# DELETE a book by ID
@bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200
