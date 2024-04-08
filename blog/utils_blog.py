from flask import flash
from blog import db
from blog.models import Entry, Comment, Category
from config import Config
    
def add_new_category(name):
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return category


def create_or_edit_post(form, user_id, entry=None):
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
            is_published=form.is_published.data,
            user_id=user_id,
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

    
def create_comment(post_id, form, user_id):
    new_comment = Comment(content=form.content.data, entry_id=post_id, user_id=user_id)
    db.session.add(new_comment)
    message = f'Comment added succesfully.'
    db.session.commit()
    flash(message, 'success')
    
    
def delete_item(user_id, item_to_delete):
    if user_id == item_to_delete.user_id or user_id == Config.admin_id:
        db.session.delete(item_to_delete)
        title = f'Post {item_to_delete.title}' if hasattr(item_to_delete, 'title') else 'Comment'
        message = f'{title} removed successfully.'
        db.session.commit()
        flash(message, 'warning')
    else:
        flash('Error. Wrong user_id', 'warning')

    
    
def search_posts_by_search_query(search_query):
    if search_query:
        return Entry.query.filter(
            (Entry.is_published == True) & (Entry.title.contains(search_query))
        ).order_by(Entry.creation_date.desc())
    else: 
        return Entry.query.filter_by(
            is_published=True
            ).order_by(Entry.creation_date.desc())
    

def search_drafts_by_search_query_and_user_id(search_query, user_id):
    if search_query:
        return Entry.query.filter(
            (Entry.is_published == False) & 
            (Entry.title.contains(search_query)) & 
            (Entry.user_id == user_id)
        ).order_by(Entry.creation_date.desc())
    else: 
        return Entry.query.filter(
            (Entry.is_published == False) & 
            (Entry.user_id == user_id)
        ).order_by(Entry.creation_date.desc())

    
    
def filter_posts_by_category(category_name=None, is_published=True):
    if category_name:
        category_filter = Category.query.filter_by(name=category_name).first()
        return Entry.query.filter(
            (Entry.is_published == is_published) &
            (Entry.category_id == category_filter.id)
        ).order_by(Entry.creation_date.desc())
    else:
        return Entry.query.filter_by(
            is_published=is_published
        ).order_by(Entry.creation_date.desc())

    
    
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