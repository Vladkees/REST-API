from flask import request
from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc

from models import Book, db
from schemas import BookSchema

class BookListResource(MethodResource, Resource):
    @doc(description="Get all books", tags=["Books"])
    @marshal_with(BookSchema(many=True))
    def get(self):
        return Book.query.all()

    @doc(description="Add a new book", tags=["Books"])
    @use_kwargs(BookSchema, location="json")
    @marshal_with(BookSchema, code=201)
    def post(self, **kwargs):
        book = Book(**kwargs)
        db.session.add(book)
        db.session.commit()
        return book, 201

class BookResource(MethodResource, Resource):
    @doc(description="Get book by ID", tags=["Books"])
    @marshal_with(BookSchema)
    def get(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        return book

    @doc(description="Delete book by ID", tags=["Books"])
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted"}, 200
