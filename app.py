from flask import Flask, render_template
import logging

def create_app():
    """
    This function is used to generate a Flask app. This is done in order to have gunicorn host the app appropriately.
    """
    app = Flask(__name__)

    # This section ties the URLs to the functions defined below.
    # For example, entering www.url.com/admin_dashboard/ should call the "home" function
    app.add_url_rule("/", 'home', home)

    # Error page routes
    # app.register_error_handler(403, page_bad_permissions)
    # app.register_error_handler(404, page_bad_route)


    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    return app

def home():
    return render_template('')


if __name__ == '__main__':
    create_app()
