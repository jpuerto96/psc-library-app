import logging

from flask import Flask, redirect, request
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app():
    """
    This function is used to generate a Flask app. This is done in order to have gunicorn host the app appropriately.
    """
    app = Flask(__name__)

    from endpoints.view_routes import authview, appview
    from endpoints.api_routes import booksapi

    from models import usersmodel, booksmodel, userbooksmodel

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = "mysql://je2l4u8j4406h8t6:yqkud6ud1p49psnd@ijj1btjwrd3b7932.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/srznofy8a4o4oavy"
    app.config[
        'SECRET_KEY'] = "hello_world!"
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'scp.library.app@gmail.com'
    app.config['MAIL_PASSWORD'] = '6u2zjdr8'
    app.config['SECURITY_PASSWORD_SALT'] = 'scplibraryapp'

    login_manager.login_view = 'login'

    app.register_blueprint(authview.auth_view_endpoints)
    app.register_blueprint(appview.app_view_endpoints)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Error page routes
    # app.register_error_handler(403, page_bad_permissions)
    # app.register_error_handler(404, page_bad_route)

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    return app


@login_manager.user_loader
def load_user(user_id):
    from models.usersmodel import UsersModel
    if user_id is not None:
        return UsersModel.query.get(int(user_id))
    return None


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login?next=' + request.path)


if __name__ == '__main__':
    create_app().run()
