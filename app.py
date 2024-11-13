
@app.route('/sign_up/')
def sign_up():
    return render_template('sign_up.html')


@app.route('/forgot_password/')
def forgot_password():
    return render_template('forgot_password.html')


@app.route('/view_trips/')
def view_trips():
    return render_template('view_trips.html')


@app.route('/account_settings/')
def account_settings():
    return render_template('account_settings.html')

