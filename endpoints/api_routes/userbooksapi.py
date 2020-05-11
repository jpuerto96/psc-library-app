from flask import Blueprint, url_for, render_template, request, current_app, Response
from flask_login import current_user, login_required
import json

from app import db
from models.userbooksmodel import UserBooksModel

user_books_api_endpoints = Blueprint('user_books_api_endpoints', __name__)


@user_books_api_endpoints.route('/user_books/', methods=['POST'])
@user_books_api_endpoints.route('/user_books/<user_book_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def user_book(user_book_id=None):
    if request.method == 'GET':
        return json.dumps(UserBooksModel.query.get(int(user_book_id)))
    elif request.method == 'POST':
        body = request.get_json(force=True)
        body['user_id'] = current_user.id
        user_book_object = UserBooksModel(**body)
        db.session.add(user_book_object)
        db.session.commit()
        return json.dumps(user_book_object.serialize())
    elif request.method == 'PUT':
        body = request.get_json(force=True)
        user_book_object = UserBooksModel.query.get(int(user_book_id))
        for key, value in user_book_object.serialize().items():
            if key in body:
                setattr(user_book_object, key, body[key])
        db.session.commit()
        return json.dumps(user_book_object.serialize())
    elif request.method == 'DELETE':
        user_book_object = UserBooksModel.query.get(int(user_book_id))
        db.session.delete(user_book_object)
        db.session.commit()
        return json.dumps({'success': True})
    else:
        return Response(status=404)
