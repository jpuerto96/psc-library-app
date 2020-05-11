import json

from flask import Blueprint, request, Response
from flask_login import current_user, login_required

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
        existing_user_book_object = UserBooksModel.query.filter_by(
            user_id=body['user_id'], book_id=body['book_id']
        ).first()
        if existing_user_book_object:
            return json.dumps({"success": False, "message": "You already own this book!"})
        user_book_object = UserBooksModel(**body)
        db.session.add(user_book_object)
        db.session.commit()
        return json.dumps(user_book_object.serialize())
    elif request.method == 'PUT':
        body = request.get_json(force=True)
        body['user_id'] = current_user.id
        user_book_object = UserBooksModel.query.get(int(user_book_id))

        if user_book_object.book_id != body['book_id']:
            existing_user_book_object = UserBooksModel.query.filter_by(
                user_id=body['user_id'], book_id=body['book_id']
            ).first()
            if existing_user_book_object:
                return json.dumps({"success": False, "message": "You already own this book!"})

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
