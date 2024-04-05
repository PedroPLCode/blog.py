import requests
import random
import os
PERSONAL_API_KEY = os.environ.get("TMDB_API_TOKEN", "")
    
def call_tmdb_api(endpoint):
    full_url = f"https://api.themoviedb.org/3/{endpoint}"
    headers = {
        "accept": "application/json",
        "Authorization": f'Bearer {PERSONAL_API_KEY}'
    }
    response = requests.get(full_url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_movies_by_list_type(list_type='popluar'):
    return call_tmdb_api(f"movie/{list_type}")


def get_movies_by_search_query(search_query):
    data = call_tmdb_api(f"search/movie?query={search_query}")
    return data['results']


def get_movies_airing_today_by_timezone(timezone):
    data = call_tmdb_api(f"tv/airing_today?timezone={timezone}")
    return data['results']


def prepare_movies_list(list_type, how_many):
    data = get_movies_by_list_type(list_type)
    data_results = data["results"]
    random.shuffle(data_results)
    return data_results[:how_many]


def get_single_movie_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"


def get_single_movie_title(movie):
    return str(movie['title'])


def get_single_movie_details(movie_id):
    return call_tmdb_api(f"movie/{movie_id}")


def get_single_movie_cast(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/credits")["cast"]


def get_single_movie_images(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/images")