from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class UsersModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    first_name = db.Column(db.String(20),
                           index=True,
                           unique=False,
                           nullable=False)
    last_name = db.Column(db.String(20),
                          index=True,
                          unique=False,
                          nullable=False)
    username = db.Column(db.String(20),
                         index=True,
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(250),
                      index=True,
                      unique=True,
                      nullable=False)
    password_hash = db.Column(db.String(250),
                              index=False,
                              unique=True,
                              nullable=False)
    is_registered = db.Column(db.Boolean,
                              index=False,
                              unique=False,
                              nullable=False,
                              default=False)
    group = db.Column(db.String(80),
                      index=False,
                      unique=False,
                      nullable=False,
                      default='User')

    books = db.relationship("UserBooksModel", back_populates="user")

    def generate_password_hash(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def is_valid_password(self, password):
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
