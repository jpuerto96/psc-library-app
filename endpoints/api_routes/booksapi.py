from flask import Blueprint, url_for, render_template, request, current_app, Response
from flask_login import current_user, login_required
import json

from app import db
from models.booksmodel import BooksModel

books_api_endpoints = Blueprint('books_api_endpoints', __name__)


@books_api_endpoints.route('/books/', methods=['GET', 'POST'])
@books_api_endpoints.route('/books/<book_id>', methods=['GET', 'PUT'])
@login_required
def book(book_id=None):
    if request.method == 'GET':
        return json.dumps(BooksModel.query.get(int(book_id)) if book_id
                          else BooksModel.query.filter_by(request.get_json()).all())
    elif request.method == 'POST':
        body = request.get_json(force=True)
        existing_book_object = BooksModel.query.filter_by(body).first()
        if existing_book_object:
            return json.dumps(existing_book_object.serialize())
        book_object = BooksModel(**body)
        db.session.add(book_object)
        db.session.commit()
        return json.dumps(book_object.serialize())
    elif request.method == 'PUT':
        body = request.get_json(force=True)
        book_object = BooksModel.query.get(int(book_id))
        for key, value in book_object.serialize().items():
            if key in body:
                setattr(book_object, key, body[key])
        db.session.commit()
        return json.dumps(book_object.serialize())
    else:
        return Response(status=404)
