import json

from flask import Blueprint, request, Response, render_template
from flask_login import current_user, login_required

from app import db
from models.userbooksmodel import UserBooksModel
from models.booksmodel import BooksModel
from plugins import email

user_books_api_endpoints = Blueprint('user_books_api_endpoints', __name__)


@user_books_api_endpoints.route('/user_books/', methods=['POST'])
@user_books_api_endpoints.route('/user_books/<user_book_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def user_book(user_book_id=None):
    """
    REST function for interacting with the user_books table.
    """
    if request.method == 'GET':
        return json.dumps(UserBooksModel.query.get(int(user_book_id)))
    elif request.method == 'POST':
        body = request.get_json(force=True)
        body['user_id'] = current_user.id
        # One should check to see whether the user_book exists already.
        existing_user_book_object = UserBooksModel.query.filter_by(
            user_id=body['user_id'], book_id=body['book_id']
        ).first()
        if existing_user_book_object:
            # If the user_book exists, return an error that you already own it.
            return json.dumps({"success": False, "message": "You already own this book!"})
        # Otherwise, construct a new user_book, insert it, and return it.
        user_book_object = UserBooksModel(**body)
        db.session.add(user_book_object)
        db.session.commit()
        return json.dumps(user_book_object.serialize())
    elif request.method == 'PUT':
        body = request.get_json(force=True)
        body['user_id'] = current_user.id
        user_book_object = UserBooksModel.query.get(int(user_book_id))

        # There are two scenarios when updating a user_book
        # 1. The book was not modified - we can simply update the user_book
        # 2. The book was modified - we must perform further validation.
        # In the case where the book was modified, we must check to see whether the "updated" book
        # has already been assigned to the user.

        # Case 2
        if user_book_object.book_id != body['book_id']:
            existing_user_book_object = UserBooksModel.query.filter_by(
                user_id=body['user_id'], book_id=body['book_id']
            ).first()
            # Case 2 - Failed validation (book has already been assigned to this user
            if existing_user_book_object:
                return json.dumps({"success": False, "message": "You already own this book!"})

        # Case 1 or Case 2 - Passed validation
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


@user_books_api_endpoints.route('/user_books/share_user_books/<email_to_send>/', methods=['GET'])
@login_required
def share_user_books(email_to_send):
    """
    Helper route for easy user book list sending.
    """
    user_books_list = UserBooksModel.query.join(BooksModel) \
        .add_columns(UserBooksModel.id, UserBooksModel.book_id, BooksModel.title, BooksModel.author,
                     UserBooksModel.date_of_purchase, UserBooksModel.notes, UserBooksModel.is_favorite) \
        .filter(UserBooksModel.user_id == current_user.id).all()

    template = render_template('email_templates/book_list_share_email.html', user_books_list=user_books_list)

    email.send_email(current_user.first_name + "'s library!", email_to_send, template)

    return json.dumps({"success": True})
