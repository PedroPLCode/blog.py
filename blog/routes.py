from flask import render_template, request, redirect, url_for, flash
from blog import app, db
#from blog.models import Author
#from blog.forms import AuthorOnlyForm, 
#from blog.utils import *

@app.route('/')
def home_page_view():
    return render_template("base.html")