from flask import render_template, request, redirect, url_for, session, flash, g
from blog import app
from blog.models import Entry
from blog.forms import EntryForm
from blog.utils import (create_or_edit_post, 
                        delete_post, 
                        search_posts_by_search_query_and_is_published
                        )
from blog.forms import LoginForm
import functools

def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions


@app.errorhandler(404)
def handle_page_not_found(error):
    return redirect(url_for("homepage_view"))


@app.context_processor
def inject_template_name():
    return {'template_name': g.get('template_name', 'unknown')}


@app.route('/')
def homepage_view():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    return render_template("homepage.html", 
                           all_posts=all_posts,
                           counter=all_posts.count()
                           )
    
    
@app.route('/search/')
def search_posts():
    search_query = request.args.get("q", "")
    posts = search_posts_by_search_query_and_is_published(search_query, True)
    return render_template("homepage.html", 
                           all_posts=posts,
                           counter=posts.count(),
                           search_query=search_query)
    

@app.route('/drafts/')
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
    return render_template("drafts.html", 
                           drafts=drafts,
                           counter=drafts.count())
    
    
@app.route('/search_drafts/')
def search_drafts():
    search_query = request.args.get("q", "")
    drafts = search_posts_by_search_query_and_is_published(search_query, False)
    return render_template("drafts.html", 
                           drafts=drafts,
                           counter=drafts.count(),
                           search_query=search_query)
    

@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_new_entry():
    form = EntryForm()
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            create_or_edit_post(form=form)
            return redirect(url_for("homepage_view"))
        else:
            errors = form.errors
    return render_template("entry_form.html", 
                           form=form, 
                           errors=errors)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
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
    return render_template("entry_form.html", 
                           form=form, 
                           entry_id=entry_id,
                           errors=errors)


@app.route("/delete-post/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    homepage = request.form.get("homepage") == "true"
    post_to_delete = Entry.query.filter_by(id=entry_id).first_or_404()
    delete_post(post_to_delete)
    return redirect(url_for("homepage_view" if homepage else "list_drafts"))


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('homepage_view'))
        else:
            errors = form.errors
            return redirect(url_for("homepage_view"))
    return render_template("login_form.html", 
                           form=form,
                           errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('homepage_view'))