from flask import flash
from faker import Faker
from blog import db
from blog.models import Entry, Comment, Category, Favorite

# USED ONLY AT THE BEGINING TO GENERATE FIRST ENTRIES.
def generate_fake_entries(how_many=12):
    fake = Faker()
    for i in range(how_many):
        new_fake_post = Entry(
            title=fake.sentence(),
            content='\n'.join(fake.paragraphs(15)),
            is_published=True
        )
        db.session.add(new_fake_post)
    db.session.commit()
    
    
def add_new_category(name):
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return category


def create_or_edit_post(form, entry=None):
    category_name = form.category.data
    category = Category.query.filter_by(name=category_name).first()
    
    if not category:
        category = add_new_category(category_name)
    
    if entry:
        entry.title = form.title.data
        entry.content = form.content.data
        entry.is_published = form.is_published.data
        
        if form.category.data == 'new category':
            category_name = form.category.data 
            category = Category(category_name)
            db.session.add(category)
        
        entry.category_id = category.id
        db.session.add(entry)
        message = f'Post {entry.title} updated successfully.'
    else:
        new_entry = Entry(
            title=form.title.data,
            content=form.content.data,
            is_published=form.is_published.data
        )
        new_entry.category = category
        db.session.add(new_entry)
        message = f'New post {new_entry.title} added successfully.'
    try:
        db.session.commit()
        flash(message, 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')

    
def create_comment(post_id, form):
    new_comment = Comment(content=form.content.data, entry_id=post_id)
    db.session.add(new_comment)
    message = f'Comment added succesfully.'
    db.session.commit()
    flash(message, 'success')
    
    
def delete_item(item_to_delete):
    db.session.delete(item_to_delete)
    title = f'Post {item_to_delete.title}' if hasattr(item_to_delete, 'title') else 'Comment'
    message = f'{title} removed succesfully.'
    db.session.commit()
    flash(message, 'warning')
    
    
def search_posts_by_search_query_and_is_published(search_query, is_published):
    if search_query:
        return Entry.query.filter(
            (Entry.is_published == is_published) & (Entry.title.contains(search_query))
        ).order_by(Entry.creation_date.desc())
    else: 
        return Entry.query.filter_by(is_published=is_published).order_by(Entry.creation_date.desc())
    
    
def filter_posts_by_category(category_name=None, is_published=True):
    if category_name:
        category_filter = Category.query.filter_by(name=category_name).first()
        return Entry.query.filter(
            (Entry.is_published == is_published) & (Entry.category_id == category_filter.id)
        ).order_by(Entry.creation_date.desc())
    else:
        return Entry.query.filter_by(is_published=is_published).order_by(Entry.creation_date.desc())
    
    
def clear_caterogies_db():
    all_entries = Entry.query.all()
    all_categories = Category.query.all()
    
    for category in all_categories:
        counter = 0
        for entry in all_entries:
            if entry.category_id == category.id:
                counter += 1
        if counter == 0:
            db.session.delete(category)
            db.session.commit()
            
            
def check_if_movies_are_in_favorites(movies):
    favorites = Favorite.query.all()
    for movie in movies:
        movie = check_and_mark_if_single_movie_is_in_favorites(movie, favorites)
    return movies


def check_and_mark_if_single_movie_is_in_favorites(movie, favorites):
    for favorite in favorites:
        if movie['id'] == favorite.movie_id:
            movie['is_favorite'] = True
    return movie