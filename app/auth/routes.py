from flask import abort, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import TemplateNotFound
from app.auth import auth
from app.instance.models.models import User
from app import database



@auth.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        # Validate password match
        if password != password2:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth.sign_up'))

        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists!', 'error')
            return redirect(url_for('auth.sign_up'))

        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        database.session.add(new_user)
        database.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/sign_up.html')



@auth.route('/forgot_password/', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if user:
            # Placeholder for sending an email with password reset instructions
            flash('Password reset instructions have been sent to your email.', 'success')
        else:
            flash('User not found.', 'error')

        return redirect(url_for('auth.forgot_password'))

    return render_template('auth/forgot_password.html')


@auth.route('/account_settings/', methods=['GET', 'POST'])
def account_settings():
    # Ensure the user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access account settings.', 'error')
        return redirect(url_for('auth.login'))

    # Retrieve the current user
    user = User.query.get(user_id)

    if request.method == 'POST':
        # Update user details
        user.username = request.form['username']
        user.email = request.form['email']
        if request.form['password']:
            user.password_hash = generate_password_hash(request.form['password'])
        database.session.commit()

        flash('Account settings updated successfully!', 'success')

    return render_template('auth/account_settings.html', user=user)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('userID')
        password = request.form.get('password')

        # Find user by username
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid username or password.", "error")
            return render_template('auth/login.html')

        # Set user session
        session['user_id'] = user.id
        session['username'] = user.username
        flash("Login successful!", "success")
        return redirect(url_for('main.index'))

    return render_template('auth/login.html')


@auth.route('/logout/')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
