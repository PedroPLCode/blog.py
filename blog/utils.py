from faker import Faker
from blog.models import Entry, db

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