import re
from flask import Flask, session, request, redirect, render_template, flash, url_for
from db.data_layer import get_user_by_email, get_user_by_id, create_user

app = Flask(__name__)
app.secret_key = 'garbage'

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate')
def authenticate():

    return render_template('authenticate.html')

@app.route('/register', methods = ['POST'])
def register():
    server_email = request.form['html_email']
    server_username = request.form['html_username']
    server_password = request.form['html_password']
    server_confirm = request.form['html_confirm']

    is_valid = True

    if server_password != server_confirm:
        flash('passwords are not the same')
        is_valid = False

    if is_empty('email', request.form):
        is_valid = False

    if is_empty('username', request.form):
        is_valid = False

    if is_empty('password', request.form):
        is_valid = False

    if not is_valid:
        return redirect(url_for('authenticate'))

    
    user = create_user(server_email, server_username, server_password)

    session['user_id'] = user.id
    session['username'] = user.name

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/login', methods = ['POST'])
def login():
    try:
        user = get_user_by_email(request.form['html_email'])
        if user.password == request.form['html_password']:
            session['user_id'] = user.id
            session['username'] = user.name
            return redirect(url_for('index'))
    except:
        pass

    flash('invalid login')
    return redirect(url_for('authenticate'))

def is_empty(name, form):
    key = 'html_{}'.format(name)
    empty = not len(form[key])>0
    if empty:
        flash('{} is empty'.format(name))
    
    return empty






app.run(debug=True, port=5001)