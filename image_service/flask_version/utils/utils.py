from random import choice
import sqlite3
import string
from werkzeug.security import generate_password_hash
from flask.globals import g
import mimetypes
from datetime import datetime

def create_user(username, firstname, lastname, password):
  """ Inserts a user record into the database """
  g.db.execute('insert into register (username, fname, lname, pwd) \
      values (?, ?, ?, ?, ?, ?)',
      [username, firstname, lastname, generate_password_hash(password)])
  # werkzeug security hash is used to secure user password
  g.db.commit()

def save_image(file):
    filename = file.filename
    imagedata = file.read()
    shorturl = hash_link()
    cur_date = datetime.now()
    ext = get_ext(filename)
    mimetype = mimetypes.types_map['.'+ext]
    g.db.execute('insert into image (filename, image, shorturl, dateadded, ext, mimetype) \
      values (?, ?, ?, ?, ?, ?)',
        [filename, sqlite3.Binary(imagedata), shorturl, cur_date, ext, mimetype])
    g.db.commit()
    return shorturl

def get_image(shorturl):
    cur = g.db.execute('select image,ext,mimetype from image where shorturl = ?',[shorturl])
    return cur.fetchone()

def get_image_data(shorturl):
    cur = g.db.execute('select filename,dateadded,ext,mimetype from image where shorturl = ?',[shorturl])
    row = cur.fetchone()
    if row:
        return dict(filename=row[0],date=row[1],ext=row[2],mimetypes=row[3],shorturl=shorturl)
    else :
        return None

def get_ext(filename) :
    return filename.split('.')[-1]

def hash_link(length=8, chars=string.letters + string.digits):
    """ Generates a random hash link
        length := length of hash to generate
        chars  := character range to be used when generating hash
    """
    return ''.join([choice(chars) for i in range(length)])

def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    sourced from : http://flask.pocoo.org/snippets/33/
    """
    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f')

    now = datetime.now()
    diff = now - dt

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
        )

    for period, singular, plural in periods:

        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default
