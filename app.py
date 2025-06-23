import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from data_manager import DataManager
from models import db


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'movies.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app

data_manager = DataManager() # Create an object of your DataManager class


@app.route('/')
def index():
    """Render the homepage with a list of all users and a form for adding new users.

    Returns:
        str: Rendered HTML template for the index page.
    """
    # Show a list of all registered users and form for adding new users (This route is GET by default)
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """Handle submission of the 'add user' form and create a new user.

    Returns:
        HTTP Response: Redirect to the index page.
    """
    name = request.form['name']
    data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    """Display a user's list of favorite movies.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: Rendered HTML template for the user's movie list.
    """
    movies = data_manager.get_movies(user_id)
    user = data_manager.get_user(user_id)
    return render_template('movies.html', movies=movies, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie to a user's list of favorite movies.

    Args:
        user_id (int): The ID of the user.

    Returns:
        HTTP Response: Redirect to the user's movie list.
    """
    title = request.form["title"]
    release_year = request.form.get('release_year')
    data_manager.add_movie(user_id, title, release_year)
    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Update the details of a specific movie in a user's list.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie to update.

    Returns:
        HTTP Response: Redirect to the user's movie list.
    """
    title = request.form["title"]
    release_year = request.form.get("release_year")
    data_manager.update_movie(movie_id, title, release_year)
    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Remove a specific movie from a user's list of favorites.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie to delete.

    Returns:
        HTTP Response: Redirect to the user's movie list.
    """
    data_manager.delete_movie(movie_id)
    return redirect(url_for('get_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """Render a custom 404 error page when a page is not found.

    Args:
        e (HTTPException): The exception raised.

    Returns:
        Tuple[str, int]: Rendered HTML template and 404 status code.
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle unexpected server errors with a JSON response.

    Args:
        e (HTTPException): The exception raised.

    Returns:
        Tuple[dict, int]: JSON error message and 500 status code.
    """
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run()