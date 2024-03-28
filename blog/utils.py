from flask import flash
from faker import Faker
from blog import db
from blog.models import Entry

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
    flash(message)
    
    
def delete_post(post_to_delete):
    db.session.delete(post_to_delete)
    message = f'Post {post_to_delete.title} removed succesfully.'
    db.session.commit()
    flash(message)
    
    
def search_posts_by_search_query_and_is_published(search_query, is_puslished):
    if search_query:
        return Entry.query.filter(
            (Entry.is_published == is_puslished) & (Entry.title.contains(search_query))
        ).order_by(Entry.creation_date.desc())
    else: 
        return Entry.query.filter_by(is_published=is_puslished).order_by(Entry.creation_date.desc())