from flask import render_template, request, redirect, url_for
from blog import app
from blog.models import Entry
from blog.forms import EntryForm
from blog.utils import create_or_edit_post

@app.errorhandler(404)
def handle_page_not_found(error):
    return redirect(url_for("homepage_view"))


@app.route('/')
def homepage_view():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/new-post/", methods=["GET", "POST"])
def create_new_entry():
   form = EntryForm()
   errors = None
   if request.method == 'POST':
       if form.validate_on_submit():
           create_or_edit_post(form=form)
           return redirect(url_for("homepage_view"))
       else:
           errors = form.errors
   return render_template("entry_form.html", form=form, errors=errors)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            create_or_edit_post(form=form, entry=entry)
            return redirect(url_for("homepage_view"))
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)