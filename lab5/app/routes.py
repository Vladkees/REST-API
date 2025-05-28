from flask import Blueprint, jsonify, request, abort
from .models import db, Book

bp = Blueprint('books', __name__, url_prefix='/books')

# Cursor pagination
@bp.route('', methods=['GET'])
def get_books():
    try:
        limit = int(request.args.get('limit', 5))
        cursor = request.args.get('cursor', None)
    except ValueError:
        return jsonify({"error": "Invalid limit or cursor"}), 400

    query = Book.query
    if cursor:
        try:
            cursor = int(cursor)
            query = query.filter(Book.id > cursor)
        except ValueError:
            return jsonify({"error": "Cursor must be an integer"}), 400

    books = query.order_by(Book.id).limit(limit).all()

    result = [{
        "id": b.id,
        "title": b.title,
        "author": b.author,
        "year": b.year
    } for b in books]

    next_cursor = result[-1]["id"] if result else None

    return jsonify({
        "data": result,
        "next_cursor": next_cursor
    })


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
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    if "id" not in data or "title" not in data or "author" not in data or "year" not in data:
        return jsonify({"error": "Missing fields"}), 400

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
