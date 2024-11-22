import sqlalchemy
from flask import abort, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from jinja2 import TemplateNotFound
from app.auth import auth
from app.auth.forms import RegistrationForm, LoginForm, ResetPasswordForm, RequestResetForm
from app import database, mail
from app.models.user import User


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

    if current_user.is_authenticated:
        return redirect(url_for('trip.plan_trip'))

    form = LoginForm()

    if form.validate_on_submit():
        user= database.session.scalar(
            sqlalchemy.select(User).where(User.username == form.username.data)
        )

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember.data)
        return redirect(url_for('trip.plan_trip'))
    return render_template('auth/login.html', title='Login', form=form)


@auth.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            send_reset_email(user, token)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main/index'))



def send_reset_email(user, token):
    msg = Message('Password Reset Request',
                  sender='noreply@example.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:{url_for(
        'auth/reset_password', token=token, _external=True)} 
        If you did not request a password reset, please ignore this email.
        '''
    mail.send(msg)


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        database.session.commit()
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/reset_password.html', form=form)



@auth.route('/sign_up/', defaults={'page': 'sign_up'})
@auth.route('/auth/<page>')
def sign_up(page):
    try:
        return render_template(f'auth/{page}.html')
    except TemplateNotFound:
        abort(404)


# @auth.route('/forgot_password/', defaults={'page': 'forgot_password'})
# @auth.route('/auth/<page>')
# def forgot_password(page):
#     try:
#         return render_template(f'auth/{page}.html')
#     except TemplateNotFound:
#         abort(404)


@auth.route('/account_settings/', defaults={'page': 'account_settings'})
@auth.route('/auth/<page>')
def account_settings(page):
    try:
        return render_template(f'auth/{page}.html')
    except TemplateNotFound:
        abort(404)
