from flask import render_template

from app.main import blueprint

@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('index.html')