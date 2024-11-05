from . import db  # Importing the database instance from the main application
from flask_login import UserMixin  # Importing UserMixin for user session management



# Event model for calendar events
class Event(db.Model):
    # Unique ID for each event
    id = db.Column(db.Integer, primary_key=True)
    # Title of the event, required with a maximum length of 150 characters
    title = db.Column(db.String(150), nullable=False)
    # Start time and date of the event, required
    start = db.Column(db.DateTime, nullable=False)
    # Optional color attribute for the event, with a maximum length of 50 characters
    color = db.Column(db.String(50))
    # Foreign key linking each event to a specific user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# User model for user authentication and account management
class User(db.Model, UserMixin):
    # Unique ID for each user
    id = db.Column(db.Integer, primary_key=True)
    # User's email, must be unique for each user, maximum length of 150 characters
    email = db.Column(db.String(150), unique=True)
    # User's password, hashed and stored as a string
    password = db.Column(db.String(150))
    # User's first name, with a maximum length of 150 characters
    first_name = db.Column(db.String(150))
    # Relationship to the Event model, allowing access to a user's events
    events = db.relationship('Event', backref='user', lazy=True)
