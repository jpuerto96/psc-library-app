import json

from flask import Blueprint, request, Response
from flask_login import login_required

from app import db
from models.booksmodel import BooksModel

books_api_endpoints = Blueprint('books_api_endpoints', __name__)


@books_api_endpoints.route('/books/', methods=['POST'])
@books_api_endpoints.route('/books/<book_id>', methods=['GET', 'PUT'])
@login_required
def book(book_id=None):
    """
    REST function for interacting with the books table.
    """
    if request.method == 'GET':
        return json.dumps(BooksModel.query.get(int(book_id)))
    elif request.method == 'POST':
        body = request.get_json(force=True)
        # One should check to see whether the book exists already.
        existing_book_object = BooksModel.query.filter_by(**body).first()
        if existing_book_object:
            # If the book exists, return that book record
            return json.dumps(existing_book_object.serialize())
        # Otherwise, construct a new book, insert it, and return it.
        book_object = BooksModel(**body)
        db.session.add(book_object)
        db.session.commit()
        return json.dumps(book_object.serialize())
    elif request.method == 'PUT':
        body = request.get_json(force=True)
        book_object = BooksModel.query.get(int(book_id))
        # Iterate over existing values and update based on body of request.
        for key, value in book_object.serialize().items():
            if key in body:
                setattr(book_object, key, body[key])
        db.session.commit()
        return json.dumps(book_object.serialize())
    else:
        return Response(status=404)
