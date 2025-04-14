import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretKeyMwahaha'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, UserGames, Games, Genres
    create_database(app)

    return app

def create_database(app):
    db_path = path.join(app.instance_path, DB_NAME)
    print(f"Checking for database at: {db_path}") # Useful for debugging

    if not path.exists(db_path):
        print(f"Database not found at {db_path}. Attempting to create...")
        try:
            # Ensure the instance directory exists
            os.makedirs(app.instance_path, exist_ok=True)
            # Create tables within the application context
            with app.app_context():
                db.create_all()
            print(f'Successfully created Database at {db_path}!')
        except Exception as e:
            # Print any errors during DB creation
            print(f"Error creating database at {db_path}: {e}")
    else:
        print(f"Database already exists at {db_path}.")
