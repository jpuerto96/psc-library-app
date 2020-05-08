from flask import Blueprint, redirect, url_for, render_template, request, make_response, flash
from flask_login import current_user, login_required, login_user, logout_user
from ..models import UserModel, Forms
from app import db, login_manager

users_endpoints = Blueprint('users_endpoints', __name__)


# Return the home page
@login_required
@users_endpoints.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@users_endpoints.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    login_form = Forms.UserLoginForm()

    if login_form.validate_on_submit():
        user = UserModel.query.filter_by(username=login_form.username.data).first()  # Validate Login Attempt
        if user and user.is_valid_password(password=login_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        flash('Invalid username/password combination')
        return redirect(url_for('home'))

    return render_template('login.html')


@users_endpoints.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return redirect((url_for('login')))


@users_endpoints.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    signup_form = Forms.UserSignupForm()

    if signup_form.validate_on_submit():
        existing_user = UserModel.query.filter_by(email=signup_form.email.data).first()
        if existing_user is None:
            user = UserModel(
                name=signup_form.name.data,
                email=signup_form.email.data,
                website=signup_form.website.data
            )
            user.generate_password_hash(signup_form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('home'))
        flash('Email address is already registered.')

    return render_template('signup.html', form=signup_form)


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return UserModel.query.get(user_id)
    return None
