from app import db


class UserBooksModel(db.Model):
    __tablename__ = 'user_books'

    id = db.Column(db.Integer,
                   primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        index=True,
                        unique=False,
                        nullable=False
                        )
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id'),
                        index=True,
                        unique=False,
                        nullable=False
                        )
    is_favorite = db.Column(db.Boolean,
                            index=False,
                            unique=False,
                            nullable=False
                            )

    user = db.relationship("UserModel", back_populates="books")
    book = db.relationship("BookModel", back_populates="users")
