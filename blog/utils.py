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