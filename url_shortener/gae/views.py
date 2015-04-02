from flask import request, redirect, url_for, render_template, g,\
      session, flash
from utils.utils import *
from werkzeug.security import check_password_hash
from application import app

@app.before_request
def before_request():
    g.logged_in = bool(session.get('logged_in'))
    g.uid = session.get('u_id') or 'anonymous'

@app.route('/')
@app.route('/<shorturl>')
def index(shorturl=None):
    error = None
    entries = None
    if shorturl is not None:
        url = searchurl(shorturl)
        if url is not None:
            return redirect(url, 301)
        else:
            error = 'Url does not exist'
    else :
        if g.uid > 1:
            entries = get_user_urls(g.uid)
    return render_template('index.html',error=error, entries=entries)

@app.route('/create', methods=['GET','POST'])
@app.route('/create/<path:longurl>', methods=['GET','POST'])
def create(longurl=None):
  """ Adds a url to the database """
  # http://finance.yahoo.com/q/op?s=BJS&m=2008-05
  longurl = longurl or request.args.get('longurl')
  longurl = join_args(longurl,request.args.lists())
  return get_url(longurl, request.headers['host'])

@app.route('/search/<shorturl>')    
def search(shorturl=None):
  """ The following function can be used to search for a shorturl/hash """
  if shorturl is None:
    error = 'No url was entered'
    return render_template('index.html', error=error)
  else:  
    return jsonurl(request.headers['host'],shorturl)

@app.route('/login', methods=['GET', 'POST'])
def login():
  """ Authenticate user credentials """
  error = None
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    user = get_user_pass(username)

    if user and check_password_hash(user.password,password) :
      session['logged_in'] = True
      session['u_id'] = user.username
      flash('You were logged in')
      return redirect(url_for('index'))
    else :
      error = 'Invalid username or password'
  return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
  """ Register/Create a new user account """
  error = None
  if request.method == 'POST':
    uname = request.form.get('username')
    firstname = request.form.get('fname')
    lastname = request.form.get('lname')
    passwd = request.form.get('password')
    spasswd =  request.form.get('spassword')
    if not uname.strip():
      error = "Username field cannot be empty"
    elif not firstname.strip():
      error = "First name field cannot be empty"
    elif not lastname.strip():
      error = "Last name field cannot be empty"
    elif user_exists(uname):
      error = "Username is already in use. Choose another"
    elif not (passwd or spasswd):
      error = 'Password field cannot be empty'
    elif spasswd != passwd:
      error = 'Passwords do not match'
    else :
      create_user(uname,firstname,lastname,passwd)
      flash("Registration was successful")
      return redirect(url_for("login"))
  return render_template('register.html',error=error)

@app.route('/logout')
def logout():
  """ Remove user session and logs a user out """
  session.pop('logged_in', None)
  session.pop('u_id', None)
  flash('You were logged out')
  return redirect(url_for('index'))
  
if __name__ == '__main__':
    app.debug = True
    app.run(port=9000)