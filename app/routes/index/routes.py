from app.routes.index import index
from flask import render_template

@index.route('/')
def home():
    return render_template('index.html')
