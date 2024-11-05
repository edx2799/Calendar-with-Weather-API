from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime  # Import datetime for date parsing
from .models import Event
from . import db

# Define the views Blueprint for handling routes related to event management
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    # Query events for the current user from the database
    user_events = Event.query.filter_by(user_id=current_user.id).all()
    
    # Format events as a list of dictionaries for easy JSON rendering
    events_list = [
        {
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),  # Convert datetime to ISO format string
            'color': event.color
        }
        for event in user_events
    ]
    
    # Render the home page with the user's events
    return render_template("home.html", events=events_list, user=current_user)

@views.route('/events', methods=['GET', 'POST'])
@login_required
def manage_events():
    if request.method == 'GET':
        # If GET request, fetch and return all events for the current user
        user_events = Event.query.filter_by(user_id=current_user.id).all()
        
        # Prepare a list of events as dictionaries
        events_list = [
            {
                'id': event.id,
                'title': event.title,
                'start': event.start.isoformat(),  # Convert datetime to ISO format string
                'color': event.color
            }
            for event in user_events
        ]
        
        # Return the list of events as a JSON response
        return jsonify(events_list)
    
    elif request.method == 'POST':
        # If POST request, add a new event
        data = request.get_json()  # Parse the JSON data from the request
        
        # Convert the 'start' string to a datetime object
        try:
            start_datetime = datetime.fromisoformat(data['start'])
        except ValueError:
            # Return error response if the datetime format is invalid
            return jsonify({'error': 'Invalid datetime format'}), 400

        # Create a new Event instance with the provided data
        new_event = Event(
            title=data['title'],
            start=start_datetime,
            color=data['color'],
            user_id=current_user.id
        )
        
        # Add the new event to the session and commit to save in the database
        db.session.add(new_event)
        db.session.commit()
        
        # Return a success response with the new event's ID
        return jsonify({'success': True, 'id': new_event.id}), 201

@views.route('/delete-event/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    # Find the event by ID and ensure it belongs to the current user
    event = Event.query.get(event_id)
    
    if event and event.user_id == current_user.id:
        # Delete the event if it exists and belongs to the user
        db.session.delete(event)
        db.session.commit()
        return jsonify({'success': True})
    else:
        # Return an error if the event is not found or not owned by the user
        return jsonify({'error': 'Event not found or unauthorized deletion'}), 404
