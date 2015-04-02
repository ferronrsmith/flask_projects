"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    firstname = ndb.StringProperty(required=True)
    lastname = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)


class Urls(ndb.Model):
    longurl = ndb.StringProperty()
    shorturl = ndb.StringProperty()
    username = ndb.StringProperty()



