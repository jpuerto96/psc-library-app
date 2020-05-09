from app import db


class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer,
                   primary_key=True)
    author = db.Column(db.String(64),
                       index=True,
                       unique=False,
                       nullable=False)
    date_of_purchase = db.Column(db.Date,
                                 index=False,
                                 unique=False,
                                 nullable=False)
    notes = db.Column(db.Text,
                      index=False,
                      unique=False,
                      nullable=True)

    users = db.relationship("UserBooksModel", back_populates="book")
