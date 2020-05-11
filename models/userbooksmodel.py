from app import db


class UserBooksModel(db.Model):
    __tablename__ = 'user_books'

    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id', name='unique_user_book'),
    )

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

    date_of_purchase = db.Column(db.Date,
                                 index=False,
                                 unique=False,
                                 nullable=True)
    notes = db.Column(db.Text,
                      index=False,
                      unique=False,
                      nullable=True)

    user = db.relationship("UsersModel", back_populates="books")
    book = db.relationship("BooksModel", back_populates="users")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "is_favorite": self.is_favorite,
            "date_of_purchase": str(self.date_of_purchase),
            "notes": self.notes
        }
