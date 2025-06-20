from models import db, User, Movie
from config import api_key

class DataManager():
# Define Crud operations as methods
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()


    def get_users(self):
        users = User.query.all()
        return users


    def get_movies(self, user_id):
        movies = Movie.query.filter(Movie.user_id == user_id).all()
        return movies


    def add_movie(self, title):
        api_poster_url = f"http://img.omdbapi.com/?apikey={api_key}&t={title}"
        api_movie_url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
        api_movie_response = requests.get(api_movie_url)
        movie_info = api_movie_response.json()
        new_movie = Movie(
            title=title,
            director=movie_info.get("Director"),
            release_year=movie_info.get("Year"),
            poster_url=api_poster_url
        )
        db.session.add(new_movie)
        db.session.commit()


    def update_movie(self, movie_id, new_title):
        movie_to_update = Movie.query.filter(Movie.movie_id == movie_id).one()
        movie_to_update.title = new_title
        db.session.commit()


    def delete_movie(self, movie_id):
        Movie.query.filter(Movie.movie_id == movie_id).delete()
        db.session.commit()
