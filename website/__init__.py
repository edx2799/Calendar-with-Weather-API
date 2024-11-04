from flask import Flask  # Importing Flask to create the application
from flask_sqlalchemy import SQLAlchemy  # Importing SQLAlchemy for database management
from os import path  # Importing path to handle file paths
from flask_login import LoginManager  # Importing LoginManager to manage user sessions

db = SQLAlchemy()  # Initializing SQLAlchemy object to be used as a database
DB_NAME = "database.db"  # Setting the name of the SQLite database file

def create_app():
    app = Flask(__name__)  # Creating a Flask application instance
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'  # Secret key for session management and security
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Database URI for connecting to SQLite
    db.init_app(app)  # Linking SQLAlchemy to the Flask app

    from .views import views  # Importing the views blueprint for main app routes
    from .auth import auth  # Importing the auth blueprint for authentication-related routes

    app.register_blueprint(views, url_prefix='/')  # Registering the main app routes with a base URL
    app.register_blueprint(auth, url_prefix='/')  # Registering authentication routes with a base URL

    from .models import User  # Importing the User model to define the database structure
    
    with app.app_context():
        db.create_all()  # Creating tables in the database if they don't exist

    # Setting up login management
    login_manager = LoginManager()  # Initializing the LoginManager for handling user logins
    login_manager.login_view = 'auth.login'  # Defining the route to redirect to when login is required
    login_manager.init_app(app)  # Linking LoginManager to the Flask app

    # User loader function to load user by ID for sessions
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Querying the User model to retrieve the user by their ID

    return app  # Returning the Flask application instance
