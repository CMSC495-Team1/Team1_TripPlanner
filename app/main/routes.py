from flask import abort, render_template
from jinja2 import TemplateNotFound
from app.main import main
from flask_login import login_required

@main.route('/')
@main.route('/index')
@login_required
def index():
    try:
        return render_template(f'main/index.html')
    except TemplateNotFound:
        abort(404)
