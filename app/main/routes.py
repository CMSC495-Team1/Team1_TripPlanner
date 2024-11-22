from flask import abort, render_template
from jinja2 import TemplateNotFound
from app.main import main


@main.route('/', defaults={'page': 'index'})
@main.route('/<page>')
def show(page):
    try:
        return render_template(f'main/{page}.html')
    except TemplateNotFound:
        abort(404)
