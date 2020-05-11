from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import current_user, login_user, logout_user

from app import db
from models.usersmodel import UsersModel
from plugins.email import send_email
from plugins.forms import UserLoginForm, UserSignupForm
from plugins.tokenizer import get_token, is_valid_token

auth_view_endpoints = Blueprint('auth_view_endpoints', __name__)


@auth_view_endpoints.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('app_view_endpoints.home'))

    login_form = UserLoginForm()

    if login_form.validate_on_submit():
        user = UsersModel.query.filter_by(username=login_form.username.data).first()
        if user and user.is_valid_password(password=login_form.password.data):
            login_user(user)
            if user.is_registered:
                next_page = request.args.get('next')
                return redirect(next_page or url_for('app_view_endpoints.home'))
            else:
                return redirect(url_for('auth_view_endpoints.register'))
        flash('Invalid username/password combination')
        return redirect(url_for('app_view_endpoints.home'))

    return render_template('login.html', form=login_form)


@auth_view_endpoints.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return redirect((url_for('auth_view_endpoints.login')))


@auth_view_endpoints.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('app_view_endpoints.home'))

    signup_form = UserSignupForm()

    if signup_form.validate_on_submit():
        existing_user = UsersModel.query.filter_by(email=signup_form.email.data).first()
        if existing_user is None:
            user = UsersModel(
                first_name=signup_form.first_name.data,
                last_name=signup_form.last_name.data,
                username=signup_form.username.data,
                email=signup_form.email.data
            )
            user.generate_password_hash(signup_form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('auth_view_endpoints.register'))
        flash('Email address is already registered.')

    return render_template('signup.html', form=signup_form)


@auth_view_endpoints.route('/register/', methods=['GET'])
@auth_view_endpoints.route('/register/<registration_token>', methods=['GET'])
def register(registration_token=None):
    if registration_token is None:
        token = get_token(current_user.email)
        registration_url = url_for('auth_view_endpoints.register', registration_token=token, _external=True)
        template = render_template('email_templates/registration_email.html', registration_url=registration_url)
        send_email("SCP Library Registration", current_user.email, template)
        logout_user()
        return render_template('register.html')
    else:
        email = is_valid_token(registration_token)
        if email:
            user = UsersModel.query.filter_by(email=email).first()
            user.is_registered = True
            db.session.commit()
            login_user(user)
            return redirect(url_for('app_view_endpoints.home'))
        else:
            return render_template('register.html')
