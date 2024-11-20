from flask import abort, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from flask_mail import Message
from jinja2 import TemplateNotFound
from app.auth import auth
from app.auth.forms import RegistrationForm, LoginForm, ResetPasswordForm, RequestResetForm
from app.instance.models.models import User
from app import database, mail


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Create a new user object
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)

        database.session.add(user)
        database.session.commit()

        flash('Your account has been created! You are now able to log in.', 'success')

        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('main/index'))
        else:
            flash('Login Unsuccessful. Please check your email and password.', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@auth.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            send_reset_email(user, token)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))
    return render_template('forgot_password.html', form=form)

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
