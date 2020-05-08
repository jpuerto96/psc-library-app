import logging

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models import UserModel

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    """
    This function is used to generate a Flask app. This is done in order to have gunicorn host the app appropriately.
    """
    app = Flask(__name__)

    from endpoints import UsersAPI, BooksAPI

    app.config[
        'SQLALCHEMY_DATABASE_URI'] = "mysql://je2l4u8j4406h8t6:yqkud6ud1p49psnd@ijj1btjwrd3b7932.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/srznofy8a4o4oavy"
    app.config[
        'SECRET_KEY'] = "hello_world!"

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(UsersAPI.users_endpoints)

    # Error page routes
    # app.register_error_handler(403, page_bad_permissions)
    # app.register_error_handler(404, page_bad_route)

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    return app


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return UserModel.query.get(int(user_id))
    return None


if __name__ == '__main__':
    create_app().run()
