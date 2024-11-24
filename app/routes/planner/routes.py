from flask import render_template
from flask_login import login_required
from app.routes.planner import planner

@planner.route('/dashboard')
@login_required
def dashboard():
    return render_template('planner/dashboard.html')
