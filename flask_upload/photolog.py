"""
photolog.py
===========
This is a simple example app for Flask-Uploads. It uses Flask-CouchDB as well,
because I like CouchDB. It's a basic photolog app that lets you submit blog
posts that are photos.
"""
import datetime
import os
from flask import (Flask, request, url_for, redirect, render_template, flash,
                   session, g)
from flaskext.mongoalchemy import MongoAlchemy
from flask.helpers import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from packages.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)
from packages.snippets import timesince, login_required
from models import *
# application

app = Flask(__name__)
app.config.from_pyfile('upload.cfg')
app.jinja_env.filters['timesince'] = timesince

# uploads

uploaded_photos = UploadSet('photos', IMAGES)
configure_uploads(app, uploaded_photos)

# mongo alchemy

db = MongoAlchemy(app)


# utils

def to_index():
    return redirect(url_for('show_entries'))


@app.before_request
def login_handle():
    g.logged_in = bool(session.get('logged_in'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show')
@login_required
def show_entries():
    uname = session.get('user_name')
    entries = File.query.filter(File.author.username == uname)
    return render_template('show_entries.html',entries=entries)

@app.route('/_delete_entry')
def delete_entry() :
    success = False
    filename = request.args.get('fname', '', type=str)
    file = File.query.filter(File.filename == filename).first()
    if file is not None:
        file.remove()
        success = True
        os.remove(file.fileabslink) # delete file from OS.^_^
    return jsonify(result=success)

# views
@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        photo = request.files.get('photo')
        title = request.form.get('title')
        caption = request.form.get('caption')
        uname = session.get('user_name')
        if not (photo and title and caption):
            flash("You must fill in all the fields")
        else:
            try:
                filename = uploaded_photos.save(photo,uname)
            except UploadNotAllowed:
                flash("The upload was not allowed")
            else:
                user = User.query.filter(User.username == session.get('user_name')).first()
                file = File(filename=filename, filepath=create_path(uname), fileabslink= create_path(uname,filename=filename),author=user, title=title, caption=caption, date=datetime.datetime.now())
                file.save()
                flash("Upload was successful")
                return to_index()
    return render_template('new.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        uname = request.form.get('username')
        passwd = request.form.get('password')

        user = User.query.filter(User.username == uname).first()

        if  not uname.strip():
            error = "Username or Password field cannot be empty"
        elif not passwd:
            error = 'Password field cannot be empty'
        elif user is None:
            error = 'Invalid username'
        elif check_password_hash(user.password,passwd):
            session['logged_in'] = True
            session['user_name'] = uname
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        else :
            error = 'Invalid password'

    return render_template('login.html',error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        uname =request.form.get('username')
        passwd = request.form.get('password')
        spasswd =  request.form.get('spassword')

        if  not uname.strip() :
            error = "Username field cannot be empty"
        elif User.query.filter(User.username == uname).first():
            error = "Username is already in use. Choose another"
        elif not (passwd or spasswd):
            error = 'Password field cannot be empty'
        elif spasswd != passwd:
            error = 'Passwords do not match'
        else :
            user = User(username=uname,password=generate_password_hash(passwd))
            user.save()
            flash("Registration was successful")
            return redirect(url_for("login"))

    return render_template('register.html',error=error)

@app.route('/logout')
def logout():
    if session.get('logged_in'):
        session['logged_in'] = False
        session['user_name'] = ''
        flash("Successfully logged out")
    else:
        flash("You weren't logged in to begin with")
    return to_index()

def create_path(name, filename=''):
    return os.curdir + '/static/files/' + filename

if __name__ == '__main__':
    app.run(debug=True)
