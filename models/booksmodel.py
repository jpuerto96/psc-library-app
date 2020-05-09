from app import db


class BooksModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String(200),
                      index=True,
                      unique=True,
                      nullable=False)
    author = db.Column(db.String(64),
                       index=True,
                       unique=False,
                       nullable=False)

    users = db.relationship("UserBooksModel", back_populates="book")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author
        }
