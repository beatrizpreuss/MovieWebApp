import os
from flask import Flask
from data_manager import DataManager
from models import db, Movie


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'movies.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app

data_manager = DataManager() # Create an object of your DataManager class


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)  # Temporarily returning users as a string



if __name__ == '__main__':#
    app.run()