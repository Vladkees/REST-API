from flask import Blueprint, jsonify, request, abort
from .models import db, Book

bp = Blueprint('books', __name__, url_prefix='/books')

@bp.route('', methods=['GET'])
def get_books():
    try:
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return jsonify({"error": "Limit and offset must be integers"}), 400

    books = Book.query.offset(offset).limit(limit).all()
    return jsonify([{
        "id": b.id,
        "title": b.title,
        "author": b.author,
        "year": b.year
    } for b in books])

@bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)
    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.year
    })

@bp.route('', methods=['POST'])
def add_book():
    data = request.get_json()
    if Book.query.get(data["id"]):
        return jsonify({"error": "Book with this ID already exists"}), 400
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return jsonify(data), 201

@bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})
