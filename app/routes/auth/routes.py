import sqlalchemy
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from app.routes.auth import auth
from app.forms.forms import RegistrationForm, LoginForm, RequestResetForm
from app import database
from app.models.user import User
from urllib.parse import urlparse


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Create a new user object
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)

        database.session.add(user)
        database.session.commit()

        flash('Your account has been created! You are now able to log in.', 'success')

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index.home'))

    # Create an instance of the login form
    form = LoginForm()

    # Check if the form is submitted and validated
    if form.validate_on_submit():
        # Query the database for the user by username
        user = database.session.scalar(
            sqlalchemy.select(User).where(User.username == form.username.data)
        )

        # If user is not found or password is incorrect, flash an error message
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))

        # Log the user in
        login_user(user, remember=form.remember.data)

        # Get the next page from the URL parameters
        next_page = request.args.get('next')

        # Validate the next URL is safe
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('planner.dashboard')

        # Flash a success message and redirect to the next page
        flash('Successfully logged in!', 'success')
        return redirect(next_page)

    # Render the login template with the form
    return render_template('auth/login.html', title='Login', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index.home'))
