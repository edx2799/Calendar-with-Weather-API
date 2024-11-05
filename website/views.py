from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from .models import Event
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    # Fetch events for the current user
    user_events = Event.query.filter_by(user_id=current_user.id).all()
    events_list = [
        {
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),
            'color': event.color
        }
        for event in user_events
    ]
    return render_template("home.html", events=events_list, user=current_user)

@views.route('/events', methods=['GET', 'POST'])
@login_required
def manage_events():
    if request.method == 'GET':
        # Fetch events for the current user
        user_events = Event.query.filter_by(user_id=current_user.id).all()
        events_list = [
            {
                'id': event.id,
                'title': event.title,
                'start': event.start.isoformat(),
                'color': event.color
            }
            for event in user_events
        ]
        return jsonify(events_list)  # Return events in JSON format
    elif request.method == 'POST':
        # Add a new event
        data = request.get_json()
        
        # Convert the 'start' string to a datetime object
        try:
            start_datetime = datetime.fromisoformat(data['start'])
        except ValueError:
            return jsonify({'error': 'Invalid datetime format'}), 400

        new_event = Event(
            title=data['title'],
            start=start_datetime,
            color=data['color'],
            user_id=current_user.id
        )
        db.session.add(new_event)  # Add the event to the database
        db.session.commit()  # Commit the changes to the database
        return jsonify({'success': True, 'id': new_event.id}), 201  # Return the new event ID

@views.route('/update-event/<int:event_id>', methods=['PUT'])
@login_required
def update_event(event_id):
    # Update an existing event
    event = Event.query.get(event_id)  # Get the event by ID
    if event and event.user_id == current_user.id:
        data = request.get_json()
        event.title = data['title']  # Update the event title
        event.start = datetime.fromisoformat(data['start'])  # Update the event start time
        event.color = data['color']  # Update the event color
        db.session.commit()  # Commit the changes to the database
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Event not found or unauthorized'}), 404

@views.route('/delete-event/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)  # Get the event by ID
    if event and event.user_id == current_user.id:
        db.session.delete(event)  # Delete the event from the database
        db.session.commit()  # Commit the changes to the database
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Event not found or unauthorized deletion'}), 404


@views.route('/weather', methods=['GET'])
@login_required
def weather():
    return render_template("weather.html", user=current_user) # Pass current_user to template of weather.html