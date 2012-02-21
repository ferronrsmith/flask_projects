#imports
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from database import db_session
from models import Blog, User



#configuration
DEBUG = True

app = Flask(__name__)
app.secret_key = 'J\x89\x04\x7f\xc7\x13<\x02\xf7\xb1O\x80\xebdQ\x85o5\x18<;J\x1b\x9a'
app.username = 'des'
app.password = 'enter'


@app.route('/')
def show_entries():
    entries = Blog.query.all()
    return render_template('show_entries.html',entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    blog = Blog(request.form['title'], request.form['text'])
    db_session.add(blog)
    db_session.commit()

    flash('New entry was successfully posted');
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        uname = username=request.form['username']
        passwd = password = request.form['password']

        user = User.query.filter_by(username=uname).first()

        if user is None:
            error = 'Invalid username'
        elif(user.check_password(passwd)):
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        else :
            error = 'Invalid password'

    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(debug=True)