from flask import abort, render_template
from jinja2 import TemplateNotFound
from app.auth import auth


@auth.route('/sign_up/', defaults={'page': 'sign_up'})
@auth.route('/auth/<page>')
def sign_up(page):
    try:
        return render_template(f'auth/{page}.html')
    except TemplateNotFound:
        abort(404)


@auth.route('/forgot_password/', defaults={'page': 'forgot_password'})
@auth.route('/auth/<page>')
def forgot_password(page):
    try:
        return render_template(f'auth/{page}.html')
    except TemplateNotFound:
        abort(404)


@auth.route('/account_settings/', defaultss={'page': 'account_settings'})
@auth.route('/auth/<page>')
def account_settings():
    try:
        return render_template(f'auth/{page}.html')
    except TemplateNotFound:
        abort(404)