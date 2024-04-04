from datetime import datetime
from blog import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, 
                              default=datetime.utcnow)
    is_published= db.Column(db.Boolean, default=False)
    comments = db.relationship("Comment", backref="entry")
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
        
        
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, 
                                default=datetime.utcnow)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    entries = db.relationship("Entry", backref="category")