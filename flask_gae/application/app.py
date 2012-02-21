#imports
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from models import Blog
from google.appengine.api import users
from google.appengine.ext import db

import cgi



#configuration
DEBUG = True

app = Flask(__name__)
app.secret_key = 'J\x89\x04\x7f\xc7\x13<\x02\xf7\xb1O\x80\xebdQ\x85o5\x18<;J\x1b\x9a'
app.username = 'des'
app.password = 'enter'


@app.route('/')
def show_entries():
    entries = db.GqlQuery("SELECT * FROM Blog")
    return render_template('show_entries.html',entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    blog = Blog()
    blog.title = cgi.escape(request.form['title'])
    blog.text = cgi.escape(request.form['text'])
    blog.put()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        uname = request.form['username']
        passwd = request.form['password']

        if uname != app.username:
            error = "Invalid username"
        elif passwd != app.password:
            error = "Invalid password"
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))

    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


    #if __name__ == '__main__':
    #    app.run(debug=True)