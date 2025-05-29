from flask import request
from flask_restful import Resource
from flasgger.utils import swag_from

books = []

class BookListResource(Resource):
    @swag_from({
        'responses': {200: {'description': 'List of books'}},
        'parameters': [],
        'tags': ['Books']
    })
    def get(self):
        return books, 200

    @swag_from({
        'responses': {201: {'description': 'Book created'}},
        'parameters': [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "author": {"type": "string"},
                        "year": {"type": "integer"}
                    },
                    "required": ["id", "title", "author", "year"]
                }
            }
        ],
        'tags': ['Books']
    })
    def post(self):
        data = request.get_json()
        if any(book['id'] == data['id'] for book in books):
            return {"message": "Book with this ID already exists"}, 400
        books.append(data)
        return data, 201

class BookResource(Resource):
    @swag_from({
        'responses': {
            200: {'description': 'Book found'},
            404: {'description': 'Book not found'}
        },
        'tags': ['Books']
    })
    def get(self, book_id):
        book = next((b for b in books if b["id"] == book_id), None)
        if book is None:
            return {"message": "Book not found"}, 404
        return book

    @swag_from({
        'responses': {
            200: {'description': 'Book deleted'},
            404: {'description': 'Book not found'}
        },
        'tags': ['Books']
    })
    def delete(self, book_id):
        global books
        book = next((b for b in books if b["id"] == book_id), None)
        if book is None:
            return {"message": "Book not found"}, 404
        books = [b for b in books if b["id"] != book_id]
        return {"message": "Book deleted"}, 200
