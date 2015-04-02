"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class Image(ndb.Model):
    filename = ndb.StringProperty(required=True)
    image = ndb.BlobProperty(required=True)
    shorturl = ndb.StringProperty(required=True)
    ext = ndb.StringProperty(required=True)
    mimetype = ndb.StringProperty(required=True)
    dateadded = ndb.StringProperty()



