from random import choice
import string
import mimetypes
from models import Image
from datetime import datetime
from google.appengine.ext import db

def save_image(file):
    filename = file.filename
    imagedata = file.read()
    shorturl = hash_link()
    ext = get_ext(filename)
    cur_date = str(datetime.now())
    mimetype = mimetypes.types_map['.'+ext]
    image = Image(filename=filename,image=db.Blob(imagedata), shorturl=shorturl, ext=ext, mimetype=mimetype, dateadded=cur_date)
    image.put()
    return shorturl


def get_image(shorturl):
    qry = Image.query(Image.shorturl == shorturl)
    image = qry.get()
    return image

def get_image_data(shorturl):
    qry = Image.query(Image.shorturl == shorturl)
    image = qry.get()
    if image:
        return dict(filename=image.filename,date=image.dateadded,ext=image.ext,mimetypes=image.mimetype,shorturl=image.shorturl)
    else :
        return None

def update_filename(filename,shorturl):
    qry = Image.query(Image.shorturl == shorturl)
    image = qry.get()
    image.filename = filename
    image.put()

def delete_image(shorturl):
    qry = Image.query(Image.shorturl == shorturl)
    image = qry.get()
    image.key.delete()

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
