from app import db


class BooksModel(db.Model):
    __tablename__ = 'books'

    __table_args__ = (
        db.UniqueConstraint('title', 'author', name='unique_title_author'),
    )

    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String(200),
                      index=True,
                      unique=False,
                      nullable=False)
    author = db.Column(db.String(64),
                       index=True,
                       unique=False,
                       nullable=False)

    users = db.relationship("UserBooksModel", back_populates="book")

    def serialize(self):
        """
        Helper function used to transform db.Model into dict. Useful for JSON serialization.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author
        }
