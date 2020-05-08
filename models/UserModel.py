from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
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
                      default='Patron')

    books = db.relationship("UserBooksModel", back_populates="books")

    def generate_password_hash(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def is_valid_password(self, password):
        return check_password_hash(self.password, password)
