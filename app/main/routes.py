from flask import render_template
from app.main import main
from flask_login import login_required

@main.route('/')
@main.route('/index')
def index():
    return render_template(f'main/index.html')
