#from datetime import datetime
from blog import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    comment = db.Column(db.String(100), index=True)
    books = db.relationship("Book", backref="author")

    def __str__(self):
        return f"<User {self.name}>"

