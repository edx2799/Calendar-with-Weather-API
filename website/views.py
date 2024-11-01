from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Event
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        event_data = request.get_json()
        new_event = Event(
            title=event_data['title'],
            start=event_data['start'],
            color=event_data['color'],
            user_id=current_user.id
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'success': True}), 201  # Respond with a success message
    
    # For GET requests, return events for the current user
    user_events = Event.query.filter_by(user_id=current_user.id).all()
    events_list = [{'id': event.id, 'title': event.title, 'start': event.start.isoformat(), 'color': event.color} for event in user_events]
    
    return render_template("home.html", events=events_list, user=current_user)  # Pass current_user to the template
