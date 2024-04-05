from blog import tmdb_client
from unittest.mock import Mock

def test_get_poster_url_uses_default_size():
    test_path = "poster-path"
    poster_url = tmdb_client.get_single_movie_poster_url(poster_api_path=test_path)
    assert poster_url == "https://image.tmdb.org/t/p/w342/poster-path"
    
    
def test_get_poster_url_uses_another_size():
    test_path = "poster-path"
    test_size = 'w666'
    poster_url = tmdb_client.get_single_movie_poster_url(poster_api_path=test_path,
                                                         size=test_size)
    assert poster_url == "https://image.tmdb.org/t/p/w666/poster-path"
   

def test_get_movies_list_type_popular():
    movies_list = tmdb_client.get_movies_by_list_type(list_type="popular")
    assert movies_list is not None
   
   
def test_get_movies_list(monkeypatch):
    mock_movies_list = ['Movie 1', 'Movie 2']
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_movies_list
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    movies_list = tmdb_client.call_tmdb_api("movie/")
    assert movies_list == mock_movies_list
    
    
def test_get_single_movie(monkeypatch):
    expected_movie_id = 123
    mock_movie_data = {'id': expected_movie_id, 'title': 'Test Movie'}
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_movie_data
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    movie = tmdb_client.get_single_movie_details(expected_movie_id)
    assert movie['id'] == expected_movie_id
    assert movie['title'] == 'Test Movie'


def test_get_movie_images(monkeypatch):
    expected_movie_id = 123
    mock_images_data = {
        'backdrops': [
            {'file_path': '/backdrop1.jpg'}, 
            {'file_path': '/backdrop2.jpg'}
        ],
        'posters': [
            {'file_path': '/poster1.jpg'}, 
            {'file_path': '/poster2.jpg'}
        ]
    }
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_images_data
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    images = tmdb_client.get_single_movie_images(expected_movie_id)
    assert len(images['backdrops']) == 2
    assert len(images['posters']) == 2


def test_get_single_movie_cast(monkeypatch):
    expected_movie_id = 123
    mock_cast_data = {
        'cast': [
            {'name': 'jas Fasola', 'character': 'test fasola'},
            {'name': 'Krol Artur', 'character': 'artur'},
            ]
        }
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_cast_data
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    cast = tmdb_client.get_single_movie_cast(expected_movie_id)
    assert len(cast) == 2
    assert cast[0]['name'] == 'jas Fasola'
    assert cast[1]['character'] == 'artur'