from blog import app
from unittest.mock import Mock
import pytest

@pytest.mark.parametrize('path, arg', (
    ('movies/', 'movie/popular'),
    ('movies/?list_type=WRONG_LIST_TYPE', 'movie/popular'),
    ('movies/?WRONG_PARAM=WRONG_LIST_TYPE', 'movie/popular'),
    ('movies/?list_type=top_rated', 'movie/top_rated'),
    ('movies/?list_type=upcoming', 'movie/upcoming'),
    ('movies/?list_type=now_playing', 'movie/now_playing'),
    ('search_movies?q=TEST_QUERY', 'search/movie?query=TEST_QUERY'),
))
def test_homepage(path, arg, monkeypatch):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("blog.tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get(path)
        assert response.status_code == 200
        api_mock.assert_called_once_with(arg)