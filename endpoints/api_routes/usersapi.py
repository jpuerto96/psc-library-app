from flask import Blueprint, url_for, render_template, request, current_app, Response
from flask_login import current_user, login_required
from models.userbooksmodel import UserBooksModel
from models.booksmodel import BooksModel
from plugins import email
import json

from app import db
from models.userbooksmodel import UserBooksModel

users_api_endpoints = Blueprint('users_api_endpoints', __name__)


@users_api_endpoints.route('/user/share_user_books/<email_to_send>/', methods=['GET'])
@login_required
def share_user_books(email_to_send):
    user_books_list = UserBooksModel.query.join(BooksModel) \
        .add_columns(UserBooksModel.id, UserBooksModel.book_id, BooksModel.title, BooksModel.author,
                     UserBooksModel.date_of_purchase, UserBooksModel.notes, UserBooksModel.is_favorite) \
        .filter(UserBooksModel.user_id == current_user.id).all()

    template = render_template('email_templates/book_list_share_email.html', user_books_list=user_books_list)

    email.send_email(current_user.first_name + "'s library!", email_to_send, template)

    current_app.logger.error(email_to_send)

    return json.dumps({"success": True})
