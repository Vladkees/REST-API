from flask import request, jsonify, current_app
from . import db
from .models import Book
from flask import current_app as app

@app.route("/books", methods=["GET"])
def get_books():
    limit = request.args.get("limit", 10, type=int)
    offset = request.args.get("offset", 0, type=int)
    books = Book.query.limit(limit).offset(offset).all()
    total = Book.query.count()
    return jsonify({
        "total": total,
        "limit": limit,
        "offset": offset,
        "books": [{"id": b.id, "title": b.title, "author": b.author} for b in books]
    })
