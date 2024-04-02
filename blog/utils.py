from flask import flash
from faker import Faker
from blog import db
from blog.models import Entry, Comment

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
    
    
def create_or_edit_post(form, entry=None):
    if entry:
        form.populate_obj(entry)
        message = f'Post {entry.title} updated succesfully.'
    else:
        new_entry = Entry(
            title=form.title.data,
            content=form.content.data,
            is_published=form.is_published.data,
        )
        db.session.add(new_entry)
        message = f'New post {new_entry.title} added succesfully.'
    db.session.commit()
    flash(message, 'success')
    
    
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
    
    
def search_posts_by_search_query_and_is_published(search_query, is_puslished):
    if search_query:
        return Entry.query.filter(
            (Entry.is_published == is_puslished) & (Entry.title.contains(search_query))
        ).order_by(Entry.creation_date.desc())
    else: 
        return Entry.query.filter_by(is_published=is_puslished).order_by(Entry.creation_date.desc())