from flask import render_template, request, redirect, url_for, flash
from blog import app, db
from blog.models import Entry
#from blog.forms import AuthorOnlyForm, 
#from blog.utils import *

@app.route('/')
def homepage_view():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    return render_template("homepage.html", all_posts=all_posts)