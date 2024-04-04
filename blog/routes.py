from flask import render_template, request, redirect, url_for, session, flash, g
from blog import app
from blog.models import Entry, Comment, Category
from blog.forms import EntryForm, CommentForm
from blog.utils import (create_or_edit_post, 
                        create_comment,
                        delete_item, 
                        search_posts_by_search_query_and_is_published,
                        filter_posts_by_category,
                        clear_caterogies_db,
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
    flash(str(error), 'danger')
    return redirect(url_for("homepage_view"))


@app.context_processor
def inject_template_name():
    return {'template_name': g.get('template_name', 'unknown')}


@app.route('/')
def homepage_view():
    clear_caterogies_db()
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    all_comments = Comment.query.all()
    all_categories = Category.query.all()
    add_comment_form = CommentForm()
    return render_template("homepage.html", 
                           all_posts=all_posts,
                           all_comments=all_comments,
                           all_categories=all_categories,
                           form=add_comment_form,
                           counter=all_posts.count()
                           )
    
    
@app.route('/search/')
def search_posts():
    clear_caterogies_db()
    all_categories = Category.query.all()
    search_query = request.args.get("q", "")
    posts = search_posts_by_search_query_and_is_published(search_query, True)
    add_comment_form = CommentForm()
    return render_template("homepage.html", 
                           all_posts=posts,
                           all_categories=all_categories,
                           counter=posts.count(),
                           form=add_comment_form,
                           search_query=search_query)
    
    
@app.route('/filter/')
def filter_posts():
    clear_caterogies_db()
    filter = request.args.get("f", "")
    all_categories = Category.query.all()
    category_names = [category.name for category in all_categories]
    
    if not filter or filter not in category_names:
        flash('Category not found.', 'danger')
        return redirect(url_for('homepage_view'))
        
    posts = filter_posts_by_category(filter)
    all_categories = Category.query.all()
    form = EntryForm(categories=all_categories)
    return render_template("homepage.html", 
                           all_posts=posts,
                           all_categories=all_categories,
                           counter=posts.count(),
                           filter=filter,
                           form=form)
    

@app.route('/drafts/')
@login_required
def list_drafts():
    clear_caterogies_db()
    all_categories = Category.query.all()
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
    return render_template("drafts.html", 
                           drafts=drafts,
                           all_categories=all_categories,
                           counter=drafts.count())
    
    
@app.route('/search_drafts/')
def search_drafts():
    clear_caterogies_db()
    all_categories = Category.query.all()
    search_query = request.args.get("q", "")
    drafts = search_posts_by_search_query_and_is_published(search_query, False)
    return render_template("drafts.html", 
                           drafts=drafts,
                           counter=drafts.count(),
                           all_categories=all_categories,
                           search_query=search_query)
    

@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_new_entry():
    all_categories = Category.query.all()
    form = EntryForm(categories=all_categories)
    errors = None
    if request.method == 'POST':
        if form.validate():
            create_or_edit_post(form=form)
            return redirect(url_for("homepage_view"))
        else:
            errors = form.errors
    return render_template("entry_form.html", 
                           form=form, 
                           errors=errors)
    
    
@app.route("/new-comment/<int:post_id>", methods=["POST"])
def create_new_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        create_comment(post_id, form=form)
    return redirect(url_for("homepage_view"))


@app.route("/delete-comment/<int:comment_id>", methods=["GET", "POST"])
@login_required
def delete_comment(comment_id):
    comment_to_delete = Comment.query.filter_by(id=comment_id).first_or_404()  
    delete_item(comment_to_delete)
    return redirect(url_for("homepage_view"))


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    all_categories = Category.query.all()
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    category = next((category for category in all_categories if category.id == entry.category_id), None)
    form = EntryForm(obj=entry, categories=all_categories, category=category)
    errors = None
        
    if request.method == 'POST':
        if form.validate():
            create_or_edit_post(form=form, entry=entry)
            return redirect(url_for("homepage_view"))
        else:
            errors = form.errors
    
    if form.category.data == 'new category':
        form.customcategory.data = '' 
        form.customcategory.render_kw = {'readonly': False, 'disabled': False}
       
    form.title.default = entry.title if entry and entry.title else None
    form.content.default = entry.content if entry and entry.content else None
    form.is_published.default = entry.is_published if entry and entry.is_published else None
    form.category.default = entry.category.name if entry and entry.category else None
    form.process()
    
    return render_template("entry_form.html", 
                           form=form, 
                           all_categories=all_categories,
                           category=category,
                           entry_id=entry_id,
                           errors=errors)


@app.route("/delete-post/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    homepage = request.form.get("homepage") == "true"
    post_to_delete = Entry.query.filter_by(id=entry_id).first_or_404()        
    delete_item(post_to_delete)
    return redirect(url_for("homepage_view" if homepage else "list_drafts"))


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST' and form.validate_on_submit():
        if form.validate_username(form.username) and form.validate_password(form.password):
            session['logged_in'] = True
            session.permanent = True
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('homepage_view'))
        else:
            errors = form.errors
            flash('Wrong username or password.', 'danger')
            redirect(url_for("login"))
    return render_template("login_form.html", 
                           form=form,
                           errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('homepage_view'))