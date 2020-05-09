from flask import current_app

from itsdangerous import URLSafeTimedSerializer


def get_token(user_email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(user_email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def is_valid_token(token, expiration=1800):
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
