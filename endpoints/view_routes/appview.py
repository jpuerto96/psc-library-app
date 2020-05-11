import json

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app import db
from models.booksmodel import BooksModel
from models.userbooksmodel import UserBooksModel

app_view_endpoints = Blueprint('app_view_endpoints', __name__)


# Return the home page
@app_view_endpoints.route('/', methods=['GET'])
@login_required
def home():
    user_books_list = UserBooksModel.query.join(BooksModel) \
        .add_columns(UserBooksModel.id, UserBooksModel.book_id, BooksModel.title, BooksModel.author,
                     UserBooksModel.date_of_purchase, UserBooksModel.notes, UserBooksModel.is_favorite) \
        .filter(UserBooksModel.user_id == current_user.id).all()
    return render_template("index.html", book_list=user_books_list)


@app_view_endpoints.route('/modal/user_books/<modal_type>/', methods=['GET'])
@app_view_endpoints.route('/modal/user_books/<modal_type>/<userbooks_id>', methods=['GET'])
@login_required
def user_books_modal(modal_type, userbooks_id=None):
    modal_template = json.load(open('./static/json_templates/modal_templates.json'))
    user_books_template = modal_template['user_books_modal']

    userbook = UserBooksModel.query.join(BooksModel) \
        .add_columns(BooksModel.title, BooksModel.author,
                     UserBooksModel.date_of_purchase, UserBooksModel.notes, UserBooksModel.is_favorite) \
        .filter(UserBooksModel.id == userbooks_id).first() if modal_type == "edit" else {}

    user_books_template['author']['options'] = []
    for author in db.session.query(BooksModel.author).distinct():
        user_books_template['author']['options'].append(author.author)

    user_books_template['title']['options'] = []
    for title in db.session.query(BooksModel.title).distinct():
        user_books_template['title']['options'].append(title.title)

    return render_template("modals/userbooks_modal.html",
                           modal_data=userbook, modal_type=modal_type, modal_template=user_books_template)
