from blog.models import Favorite
            
def check_if_movies_are_in_favorites(user_id, movies):
    favorites = Favorite.query.filter(Favorite.user_id == user_id).all()
    for movie in movies:
        movie = check_and_mark_if_single_movie_is_in_favorites(movie, favorites)
    return movies


def check_and_mark_if_single_movie_is_in_favorites(movie, favorites):
    for favorite in favorites:
        if movie['id'] == favorite.movie_id:
            movie['is_favorite'] = True
    return movie