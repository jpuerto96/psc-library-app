import logging

from flask import Flask, redirect, request
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import QueuePool

db = SQLAlchemy(engine_options={"pool_size": 10, "poolclass": QueuePool, "pool_pre_ping": True})
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app():
    """
    This function is used to generate a Flask app. This is done in order to have gunicorn host the app appropriately.
    """
    app = Flask(__name__)

    from endpoints.view_routes import authview, appview
    from endpoints.api_routes import usersapi, booksapi, userbooksapi

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = "mysql://b001ef2190521b:760ab114@us-cdbr-east-06.cleardb.net/heroku_824761ced642879"
    app.config['SECRET_KEY'] = "psclibraryapp"
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'psc.library.app@gmail.com'
    app.config['MAIL_PASSWORD'] = '9z8ve6zf'
    app.config['SECURITY_PASSWORD_SALT'] = 'psclibraryapp'
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    login_manager.login_view = 'auth_view_endpoints.login'

    app.register_blueprint(authview.auth_view_endpoints)
    app.register_blueprint(appview.app_view_endpoints)

    app.register_blueprint(usersapi.users_api_endpoints)
    app.register_blueprint(booksapi.books_api_endpoints)
    app.register_blueprint(userbooksapi.user_books_api_endpoints)

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
