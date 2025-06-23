from models import db, User, Movie
from config import api_key
from sqlalchemy.exc import SQLAlchemyError
import requests


class DataManager():
    def create_user(self, name):
        """Create and save a new user to the database.

        Args:
            name (str): The name of the user.

        Returns:
            User: The newly created User object if successful.
            None: If an error occurred.
        """
        new_user = User(name=name)
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            print("An error has occurred while creating user: ", str(e))


    def get_users(self):
        """Retrieve all users from the database.

        Returns:
            list[User]: A list of User objects.
            None: If an error occurred.
        """
        try:
            users = User.query.all()
            return users
        except SQLAlchemyError as e:
            print("A database error occurred:", str(e))
            return None
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            return None


    def get_user(self, user_id):
        """Retrieve a single user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The User object if found.
            None: If the user does not exist or an error occurred.
        """
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            print("A database error occurred:", str(e))
            return None
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            return None


    def delete_user(self, user_id):
        """
        Deletes a user from the database by their user ID.

        Args:
            user_id (int): The unique identifier of the user to delete.

        Returns:
            bool: True if a user was successfully deleted, False otherwise.
        """
        try:
            user_deleted = User.query.filter(User.user_id == user_id).delete()
            db.session.commit()
            return user_deleted > 0 # returns True if a user was deleted
        except Exception as e:
            db.session.rollback()
            print("An error has occurred while deleting user: ", str(e))
            return False


    def get_movies(self, user_id):
        """Retrieve all movies associated with a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[Movie]: A list of Movie objects associated with the user.
            None: If an error occurred.
        """
        try:
            movies = Movie.query.filter(Movie.user_id == user_id).all()
            return movies
        except SQLAlchemyError as e:
            print("A database error occurred:", str(e))
            return None
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            return None


    def add_movie(self, user_id, title, release_year):
        """Add a new movie to a user's favorites using OMDB data.

        Args:
            user_id (int): The ID of the user.
            title (str): The title of the movie.
            release_year (str or None): The release year of the movie.

        Returns:
            Movie: The newly created Movie object if successful.
            None: If an error occurred or the movie was not found.
        """
        api_movie_url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
        try:
            api_movie_response = requests.get(api_movie_url)
            api_movie_response.raise_for_status()  # raises HTTPError if response is bad
            movie_info = api_movie_response.json()
        except requests.RequestException as e:
            print("Failed to fetch movie from OMDB:", str(e))
            return None

        if movie_info.get("Response") == "False":
            print("OMDB Error:", movie_info.get("Error"))
            return None

        new_movie = Movie(
            title=title,
            director=movie_info.get("Director"),
            release_year=movie_info.get("Year"),
            poster_url=movie_info.get("Poster"),
            user_id=user_id
        )
        try:
            db.session.add(new_movie)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("An error has occurred while creating movie: ", str(e))
            return None

        return new_movie


    def update_movie(self, movie_id, new_title, release_year):
        """Update an existing movie's details using OMDB data.

        Args:
            movie_id (int): The ID of the movie to update.
            new_title (str): The new title to search in OMDB.
            release_year (str or None): Optional release year to update.

        Returns:
            Movie: The updated Movie object if successful.
            None: If the movie is not found or an error occurred.
        """
        movie = Movie.query.get(movie_id)
        if not movie:
            return

        api_movie_url = f"http://www.omdbapi.com/?apikey={api_key}&t={new_title}"
        try:
            response = requests.get(api_movie_url)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print("Failed to fetch movie from OMDB:", str(e))
            return None

        if data.get("Response") == "False":
            print("OMDB Error:", data.get("Error"))
            return None

        movie.title = new_title
        movie.director = data.get("Director")
        movie.release_year = release_year or data.get("Year")
        movie.poster_url = data.get("Poster")

        try:
            db.session.commit()
            return movie
        except Exception as e:
            db.session.rollback()
            print("An error has occurred while updating movie: ", str(e))
            return None


    def delete_movie(self, movie_id):
        """Delete a movie from the database.

        Args:
            movie_id (int): The ID of the movie to delete.

        Returns:
            bool: True if a movie was successfully deleted, False otherwise.
        """
        try:
            movie_deleted = Movie.query.filter(Movie.movie_id == movie_id).delete()
            db.session.commit()
            return movie_deleted > 0 # returns True if a movie was deleted
        except Exception as e:
            db.session.rollback()
            print("An error has occurred while deleting movie: ", str(e))
            return False

