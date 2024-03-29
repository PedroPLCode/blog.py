from blog import app
from unittest.mock import Mock
import pytest

"""
@pytest.mark.parametrize('path, arg', (
    ('/', 'movie/popular'),
    ('/?list_type=WRONG_LIST_TYPE', 'movie/popular'),
    ('/?WRONG_PARAM=WRONG_LIST_TYPE', 'movie/popular'),
    ('/?list_type=top_rated', 'movie/top_rated'),
    ('/?list_type=upcoming', 'movie/upcoming'),
    ('/?list_type=now_playing', 'movie/now_playing'),
    ('/search?q=TEST_QUERY', 'search/movie?query=TEST_QUERY'),
    ('/today?timezone=TEST_QUERY', 'tv/airing_today?timezone=TEST_QUERY'),
))
"""

#Czy @login_required przekierowuje do widoku login, przekazując mu parametr next?
def test_login_required_redirects_to_view_with_next_param():
    pass

#Czy widok dodawania, modyfikacji i usuwania wpisu wymaga logowania?
def test_login_required_to_create_new_entry():
    pass

def test_login_required_to_edit_entry():
    pass

def test_login_required_to_delete_entry():
    pass

#Czy widok szkiców wymaga logowania?
def test_login_required_to_get_list_drafts():
    pass

#Czy widok szkiców pokazuje tylko szkice?
def test_only_not_published_in_list_drafts():
    pass

#Czy na stronie głównej znajdują się jedynie opublikowane materiały?
def test_only_published_in_homepage_view():
    pass

#Czy aplikacja zwraca błąd 404, jeśli odwołamy się do nieistniejącego id posta, w widoku edycji?    
def test_error_404_if_edit_not_existing_post():
    pass