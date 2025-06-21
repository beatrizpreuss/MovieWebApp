from models import db, User, Movie
from config import api_key
import requests


class DataManager():
# Define Crud operations as methods
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()


    def get_users(self):
        users = User.query.all()
        return users


    def get_user(self, user_id):
    # For movies.html in get_movies (app.py)
        return User.query.get(user_id)


    def get_movies(self, user_id):
        movies = Movie.query.filter(Movie.user_id == user_id).all()
        return movies


    def add_movie(self, user_id, title, release_year):
        api_movie_url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
        api_movie_response = requests.get(api_movie_url)
        movie_info = api_movie_response.json()
        new_movie = Movie(
            title=title,
            director=movie_info.get("Director"),
            release_year=movie_info.get("Year"),
            poster_url=movie_info.get("Poster"),
            user_id=user_id
        )
        db.session.add(new_movie)
        db.session.commit()


    def update_movie(self, movie_id, new_title, release_year):
        movie = Movie.query.get(movie_id)
        if not movie:
            return

        api_movie_url = f"http://www.omdbapi.com/?apikey={api_key}&t={new_title}"
        response = requests.get(api_movie_url)
        data = response.json()

        movie.title = new_title
        movie.director = data.get("Director")
        movie.release_year = release_year or data.get("Year")
        movie.poster_url = data.get("Poster")

        db.session.commit()


    def delete_movie(self, movie_id):
        Movie.query.filter(Movie.movie_id == movie_id).delete()
        db.session.commit()
