from datetime import datetime
from blog import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_published= db.Column(db.Boolean, default=False)

    def __str__(self):
        return (f"<Entry\n"
                f"id: {self.id}\n"
                f"title: {self.title}\n"
                f"content: {self.content}\n"
                f"creation_date: {self.creation_date}\n"
                f"is_published: {self.is_published}>"
                )