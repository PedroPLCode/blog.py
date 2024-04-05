from flask import render_template, request, redirect, url_for, session, flash, g
from blog import app
from blog.models import Entry, Comment, Category, Favorite
from blog.forms import EntryForm, CommentForm
from blog.utils import *
from blog.forms import LoginForm
import functools
import random
from blog import tmdb_client

app.secret_key = b'my-secret-key'
LIST_TYPES = ['top_rated', 'upcoming', 'popular', 'now_playing']


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
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
    all_comments = Comment.query.all()
    all_categories = Category.query.all()
    add_comment_form = CommentForm()
    return render_template("homepage.html", 
                           all_posts=all_posts,
                           all_comments=all_comments,
                           all_categories=all_categories,
                           form=add_comment_form,
                           all_posts_counter=all_posts.count(),
                           drafts_counter=drafts.count(),
                           )
    
    
@app.route('/search/')
def search_posts():
    clear_caterogies_db()
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
    all_categories = Category.query.all()
    search_query = request.args.get("q", "")
    posts = search_posts_by_search_query_and_is_published(search_query, True)
    add_comment_form = CommentForm()
    return render_template("homepage.html", 
                           all_posts=posts,
                           all_categories=all_categories,
                           counter=posts.count(),
                           all_posts_counter=all_posts.count(),
                           drafts_counter=drafts.count(),
                           form=add_comment_form,
                           search_query=search_query,
                           )
    
    
@app.route('/filter/')
def filter_posts():
    clear_caterogies_db()
    filter = request.args.get("f", "")
    all_categories = Category.query.all()
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
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
                           all_posts_counter=all_posts.count(),
                           drafts_counter=drafts.count(),
                           filter=filter,
                           form=form
                           )
    

@app.route('/drafts/')
@login_required
def list_drafts():
    clear_caterogies_db()
    all_categories = Category.query.all()
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
    return render_template("drafts.html", 
                           drafts=drafts,
                           all_categories=all_categories,
                           all_posts_counter=all_posts.count(),
                           drafts_counter=drafts.count(),
                           )
    
    
@app.route('/search_drafts/')
def search_drafts():
    clear_caterogies_db()
    all_categories = Category.query.all()
    search_query = request.args.get("q", "")
    drafts = search_posts_by_search_query_and_is_published(search_query, False)
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    return render_template("drafts.html", 
                           drafts=drafts,
                           counter=drafts.count(),
                           all_posts_counter=all_posts.count(),
                           drafts_counter=drafts.count(),
                           all_categories=all_categories,
                           search_query=search_query,
                           )
    

@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_new_entry():
    all_categories = Category.query.all()
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
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
                           all_categories=all_categories,
                           counter=all_posts.count(),
                           all_posts_counter=all_posts.count(),
                           drafts_counter=drafts.count(),
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
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
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
                           all_posts_counter=all_posts.count(),
                           drafts_counter=drafts.count(),
                           errors=errors)


@app.route("/delete-post/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    homepage = request.form.get("homepage") == "true"
    post_to_delete = Entry.query.filter_by(id=entry_id).first_or_404()        
    delete_item(post_to_delete)
    return redirect(url_for("homepage_view" if homepage else "list_drafts"))


@app.route('/movies/')
def movies_homepage():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    all_categories = Category.query.all()
    
    selected_list = request.args.get('list_type', 'popular')
    if selected_list not in LIST_TYPES:
        selected_list = "popular"
        
    movies = tmdb_client.prepare_movies_list(how_many=8, list_type=selected_list)
    movies = check_if_movies_are_in_favorites(movies)
    
    return render_template("movies.html",
                           movies=movies,
                           current_list=selected_list,
                           list_types=LIST_TYPES,
                           all_categories=all_categories,
                           counter=all_posts.count(),
                           all_posts_counter=all_posts.count(),
                           drafts_counter=drafts.count(),
                           )
    
    
@app.route('/search_movies')
def search():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
    all_categories = Category.query.all()
    
    search_query = request.args.get("q", "")
    if search_query:
        movies = tmdb_client.get_movies_by_search_query(search_query)
    else: 
        movies = []
    movies = check_if_movies_are_in_favorites(movies)
    
    return render_template("search_movies.html",
                           movies=movies,
                           movies_counter=len(movies),
                           all_categories=all_categories,
                           search_query=search_query,
                           all_posts_counter=all_posts.count(),
                           drafts_counter=drafts.count(),
                           )
    

@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    all_categories = Category.query.all()
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
    details = tmdb_client.get_single_movie_details(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    movie_images = tmdb_client.get_single_movie_images(movie_id)
    random_image = random.choice(movie_images['backdrops']) if movie_images['backdrops'] else None
    favorites = Favorite.query.all()    
    movie = check_and_mark_if_single_movie_is_in_favorites(details, favorites)
    
    return render_template("movie_details.html",
                           movie=movie,
                           cast=cast,
                           image=random_image,
                           all_categories=all_categories,
                           all_posts_counter=all_posts.count(),
                           drafts_counter=drafts.count(),
                           )
    

@app.route("/favorites/add", methods=['POST'])
@login_required
def add_to_favorites():
    referer = request.headers.get('Referer')
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        favorites = Favorite.query.all()
        for favorite in favorites:
            if favorite.movie_id == int(movie_id):
                flash(f'"{movie_title}" already in Favorites!')
                return redirect(referer if referer else url_for('homepage'))
                
        new_favorite = Favorite(movie_id=movie_id, movie_title=movie_title)
        db.session.add(new_favorite)
        db.session.commit()
        flash(f'"{movie_title}" saved in Favorites!')
        
    return redirect(referer if referer else url_for('movies_homepage'))


@app.route("/favorites/delete", methods=['POST'])
@login_required
def delete_from_favorites():
    referer = request.headers.get('Referer')            
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        favorites = Favorite.query.all()
        for favorite in favorites:
            if favorite.movie_id  == int(movie_id):
                db.session.delete(favorite)
                db.session.commit()
        flash(f'"{movie_title}" removed from Favorites!')
  
    return redirect(referer if referer else url_for('favorites'))


@app.route('/favorites/')
@login_required
def favorites():
    all_categories = Category.query.all()
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
    favorites = Favorite.query.all()
    movies = []
    for favorite in favorites:
        movies.append(tmdb_client.get_single_movie_details(favorite.movie_id))
    return render_template("favorites.html",
                            movies=movies,
                            all_categories=all_categories,
                            all_posts_counter=all_posts.count(),
                            drafts_counter=drafts.count(),
                            )
    

@app.route("/login/", methods=['GET', 'POST'])
def login():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.creation_date.desc())
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.creation_date.desc())
    all_categories = Category.query.all()
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
                           all_categories=all_categories,
                           all_posts_counter=all_posts.count(),
                           drafts_counter=drafts.count(),
                           errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('homepage_view'))


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_single_movie_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.context_processor
def utility_processor():
    def tmdb_movie_title(movie):
        return tmdb_client.get_single_movie_title(movie)
    return {"tmdb_movie_title": tmdb_movie_title}


@app.context_processor
def utility_processor():
    def favorites_counter():
        favorites = Favorite.query.all()
        return len(favorites)
    return {"favorites_counter": favorites_counter}


if __name__ == '__main__':
    app.run(debug=True)