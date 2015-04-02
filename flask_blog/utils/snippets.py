from datetime import datetime
from functools import wraps
from flask import g, redirect, url_for

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

def login_required(f):
    """
     sourced and modified decorator from : http://flask.pocoo.org/docs/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.logged_in is (None or False):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function