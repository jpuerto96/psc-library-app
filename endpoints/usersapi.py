from flask import Blueprint, redirect, url_for, render_template, request, flash, current_app
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from models.forms import UserLoginForm, UserSignupForm
from models.usersmodel import UserModel

users_endpoints = Blueprint('users_endpoints', __name__)


# Return the home page
@users_endpoints.route('/', methods=['GET'])
@login_required
def home():
    return render_template("index.html")


@users_endpoints.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users_endpoints.home'))

    login_form = UserLoginForm()

    if login_form.validate_on_submit():
        user = UserModel.query.filter_by(username=login_form.username.data).first()  # Validate Login Attempt
        if user and user.is_valid_password(password=login_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('users_endpoints.home'))
        flash('Invalid username/password combination')
        return redirect(url_for('users_endpoints.home'))

    return render_template('login.html', form=login_form)


@users_endpoints.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return redirect((url_for('users_endpoints.login')))


@users_endpoints.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('users_endpoints.home'))

    signup_form = UserSignupForm()

    if signup_form.validate_on_submit():
        existing_user = UserModel.query.filter_by(email=signup_form.email.data).first()
        if existing_user is None:
            user = UserModel(
                username=signup_form.username.data,
                email=signup_form.email.data
            )
            user.generate_password_hash(signup_form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('users_endpoints.home'))
        flash('Email address is already registered.')

    return render_template('signup.html', form=signup_form)
