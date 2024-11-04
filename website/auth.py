from flask import Blueprint, render_template, request, flash, redirect, url_for  # Importing necessary Flask modules
from .models import User  # Importing the User model for database queries
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing and checking
from . import db  # Importing the database instance
from flask_login import login_user, login_required, logout_user, current_user  # For user session management

# Initializing the Blueprint for authentication routes
auth = Blueprint('auth', __name__)

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If the request is a POST, the user is trying to log in
    if request.method == 'POST':
        email = request.form.get('email')  # Getting email from form
        password = request.form.get('password')  # Getting password from form

        # Querying the database to find the user by email
        user = User.query.filter_by(email=email).first()
        if user:
            # Checking if the provided password matches the stored hashed password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')  # Success message
                login_user(user, remember=True)  # Logging in the user and setting session
                return redirect(url_for('views.home'))  # Redirecting to home page
            else:
                flash('Incorrect password, try again.', category='error')  # Error if password is wrong
        else:
            flash('Email does not exist.', category='error')  # Error if email is not registered

    # Rendering login template with current user info
    return render_template("login.html", user=current_user)

# Logout route
@auth.route('/logout')
@login_required  # Ensuring user is logged in to log out
def logout():
    logout_user()  # Logging out the current user
    return redirect(url_for('auth.login'))  # Redirecting to login page

# Sign-up route
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # If the request is a POST, the user is attempting to sign up
    if request.method == 'POST':
        email = request.form.get('email')  # Getting email from form
        first_name = request.form.get('firstName')  # Getting first name from form
        password1 = request.form.get('password1')  # Getting password from form
        password2 = request.form.get('password2')  # Getting password confirmation

        # Validating form inputs
        user = User.query.filter_by(email=email).first()  # Checking if email is already registered
        if user:
            flash('Email already exists.', category='error')  # Error if email exists
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')  # Error if email is too short
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')  # Error if name is too short
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')  # Error if passwords don't match
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')  # Error if password is too short
        else:
            # Creating a new user with hashed password if inputs are valid
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)  # Adding new user to the database session
            db.session.commit()  # Committing session to save user to the database
            login_user(new_user, remember=True)  # Logging in the new user
            flash('Account created!', category='success')  # Success message
            return redirect(url_for('views.home'))  # Redirecting to home page

    # Rendering sign-up template with current user info
    return render_template("sign_up.html", user=current_user)
