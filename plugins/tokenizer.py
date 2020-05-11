from flask import current_app

from itsdangerous import URLSafeTimedSerializer


def get_token(user_email):
    """
    Function used to generate a token based on the user email address, with time expiration.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(user_email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def is_valid_token(token, expiration=1800):
    """
    Function used to check whether a token is valid based on expiration.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email
