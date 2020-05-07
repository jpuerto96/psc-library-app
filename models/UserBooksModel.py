from app import db
from sqlalchemy import ForeignKey


class UserBooksModel(db.Model):
    __tablename__ = 'user_books'

    id = db.Column(db.Integer,
                   primary_key=True)
    user_id = db.Column(db.Integer,
                        index=True,
                        unique=False,
                        nullable=False,
                        ForeignKey=db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer,
                        index=True,
                        unique=False,
                        nullable=False,
                        ForeignKey=db.ForeignKey('books.id'))
    is_favorite = db.Column(db.Boolean,
                            index=False,
                            unique=False,
                            nullable=False)

    user = db.relationship("UserModel", back_populates="books")
    book = db.relationship("BookModel", back_populates="users")

