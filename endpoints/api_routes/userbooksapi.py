from flask import Blueprint, url_for, render_template, request, current_app, Response
import json

from app import db
from models.userbooksmodel import UserBooksModel

user_books_api_endpoints = Blueprint('user_books_api_endpoints', __name__)


@user_books_api_endpoints.route('/user_books/', methods=['GET', 'POST'])
@user_books_api_endpoints.route('/user_books/<user_book_id>', methods=['GET', 'PUT', 'DELETE'])
def user_book(user_book_id=None):
    if request.method == 'GET':
        return json.dumps(UserBooksModel.query.get(int(user_book_id)) if user_book_id
                          else UserBooksModel.query.filter_by(request.get_json()).all())
    elif request.method == 'POST':
        body = request.get_json(force=True)
        current_app.logger.error(body)
        user_book_object = UserBooksModel(**body)
        db.session.add(user_book_object)
        db.session.commit()
        return json.dumps(user_book_object.serialize())
    elif request.method == 'PUT':
        body = request.get_json(force=True)
        user_book_object = UserBooksModel.query.get(int(user_book_id))
        for key, value in user_book_object.iteritems():
            if body[key]:
                setattr(user_book_object, key, body[key])
        db.session.commit()
        return json.dumps(user_book_object.serialize)
    elif request.method == 'DELETE':
        return json.dumps({"success": True})
    else:
        return Response(status=404)
