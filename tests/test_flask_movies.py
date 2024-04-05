from blog import app
from unittest.mock import Mock
import pytest

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
def test_homepage(path, arg, monkeypatch):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get(path)
        assert response.status_code == 200
        api_mock.assert_called_once_with(arg)