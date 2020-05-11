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
    """
    Function that loads the login page and handles logging a user in.
    """
    # If user is already logged in, send them to the home page.
    if current_user.is_authenticated:
        return redirect(url_for('app_view_endpoints.home'))

    # Generate a form to log in.
    login_form = UserLoginForm()

    if login_form.validate_on_submit():
        # Get the user
        user = UsersModel.query.filter_by(username=login_form.username.data).first()
        if user and user.is_valid_password(password=login_form.password.data):
            # If the password is valid, log the user in
            login_user(user)
            # If the user has already registered their e-mail, send them home.
            # Otherwise send them to registration page.
            if user.is_registered:
                next_page = request.args.get('next')
                return redirect(next_page or url_for('app_view_endpoints.home'))
            else:
                return redirect(url_for('auth_view_endpoints.register'))

    return render_template('login.html', form=login_form)


@auth_view_endpoints.route('/logout/', methods=['GET'])
def logout():
    """
    Function used to log a user out.
    """
    logout_user()
    return redirect((url_for('auth_view_endpoints.login')))


@auth_view_endpoints.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    Function used to load the signup page and sign a user up.
    """
    # If user is already logged in, send them home
    if current_user.is_authenticated:
        return redirect(url_for('app_view_endpoints.home'))

    # Generate a form to sign up.
    signup_form = UserSignupForm()

    if signup_form.validate_on_submit():
        # Check if e-mail already exists
        existing_user = UsersModel.query.filter_by(email=signup_form.email.data).first()
        if existing_user is None:
            # Create a user if e-mail doesn't exist already, then add them to DB.
            user = UsersModel(
                first_name=signup_form.first_name.data,
                last_name=signup_form.last_name.data,
                username=signup_form.username.data,
                email=signup_form.email.data
            )
            user.generate_password_hash(signup_form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            # Send the user to registration page.
            return redirect(url_for('auth_view_endpoints.register'))

    return render_template('signup.html', form=signup_form)


@auth_view_endpoints.route('/register/', methods=['GET'])
@auth_view_endpoints.route('/register/<registration_token>', methods=['GET'])
def register(registration_token=None):
    """
    Function that loads registration page, and registers user when following e-mail.
    """
    if registration_token is None:
        # If they are being sent here with no token, generate a token and send them e-mail
        token = get_token(current_user.email)
        registration_url = url_for('auth_view_endpoints.register', registration_token=token, _external=True)
        template = render_template('email_templates/registration_email.html', registration_url=registration_url)
        send_email("SCP Library Registration", current_user.email, template)
        logout_user()
        return render_template('register.html')
    else:
        # Check if valid token
        email = is_valid_token(registration_token)
        if email:
            # If valid token, get user, set them to registered, and log them in.
            user = UsersModel.query.filter_by(email=email).first()
            if user:
                user.is_registered = True
                db.session.commit()
                login_user(user)
                return redirect(url_for('app_view_endpoints.home'))
        else:
            return render_template('register.html')
