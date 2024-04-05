import pytest
from flask import url_for
from blog import app, db
from blog.models import Entry

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client
            
            
@pytest.mark.parametrize(('redirects', 'code', 'location'), (
    (True, 200, None),
    (False, 302, '/'),
))
def test_wrong_path_return_codes_and_redirects_location(client, redirects, code, location):
    response = client.get('/WRONG_PATH', follow_redirects=redirects)
    assert response.status_code == code
    assert response.location == location
            
            
@pytest.mark.parametrize('path', (
    ('/drafts/'),
    ('/new-post/'),
    ('/edit-post/1'),
))
def test_login_required_redirects_to_login_when_method_GET(client, path):
    response = client.get(path)
    assert response.status_code == 302
    assert response.location.endswith(url_for('login', next=path))


def test_login_required_redirects_to_login_when_method_POST(client):
    response = client.post('/delete-post/1', data={'homepage': 'false'})
    assert response.status_code == 302
    assert response.location.endswith(url_for('login', next='/delete-post/1'))


def test_homepage_shows_only_published_entries_and_drafts_shows_only_drafts(client):
    draft_test_entry = Entry(title="Draft Test 1", 
                             content="Draft content test 1", 
                             is_published=False,
                             )
    published_test_entry = Entry(title="Published Test 1", 
                                 content="Published content test 1", 
                                 is_published=True,
                                 )
    db.session.add(draft_test_entry)
    db.session.add(published_test_entry)
    db.session.commit()
    
    with client.session_transaction() as session:
        session['logged_in'] = True
        
    response_drafts = client.get('/drafts/', follow_redirects=True)
    assert response_drafts.status_code == 200
    assert b"Draft Test 1" in response_drafts.data
    assert b"Draft content test 1" in response_drafts.data
    assert b"Published Test 1" not in response_drafts.data
    assert b"Published content test 1" not in response_drafts.data
    
    response_posts = client.get('/')
    assert response_posts.status_code == 200
    assert b"Draft Test 1" not in response_posts.data
    assert b"Draft content test 1" not in response_posts.data
    assert b"Published Test 1" in response_posts.data
    assert b"Published content test 1" in response_posts.data
    
    db.session.delete(draft_test_entry)
    db.session.delete(published_test_entry)
    db.session.commit()