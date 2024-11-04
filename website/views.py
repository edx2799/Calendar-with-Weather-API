from flask import Blueprint, render_template, request, jsonify  # Import necessary modules for routing, rendering, and JSON responses
from flask_login import login_required, current_user  # Import login utilities to restrict access to authenticated users
from .models import Event  # Import the Event model to interact with the database
from . import db  # Import the database instance for database operations
import json  # Import json for handling JSON data

# Define a new blueprint for views
views = Blueprint('views', __name__)

# Route for the home page, handles both GET and POST requests
@views.route('/', methods=['GET', 'POST'])
@login_required  # Ensures only logged-in users can access this route
def home():
    # Handle POST request to add a new event
    if request.method == 'POST':
        # Get JSON data from the request
        event_data = request.get_json()
        
        # Create a new Event instance with data from the form and current user's ID
        new_event = Event(
            title=event_data['title'],
            start=event_data['start'],
            color=event_data['color'],
            user_id=current_user.id
        )
        
        # Add the new event to the database and commit the transaction
        db.session.add(new_event)
        db.session.commit()
        
        # Respond with a success message and 201 status code
        return jsonify({'success': True}), 201

    # Handle GET request to retrieve current user's events
    user_events = Event.query.filter_by(user_id=current_user.id).all()
    
    # Prepare a list of events with necessary fields formatted for JSON
    events_list = [{'id': event.id, 'title': event.title, 'start': event.start.isoformat(), 'color': event.color} for event in user_events]
    
    # Render the home template, passing the events and current user as context
    return render_template("home.html", events=events_list, user=current_user)
