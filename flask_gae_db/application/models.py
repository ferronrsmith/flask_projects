from google.appengine.ext import db

class Blog(db.Model):
	title = db.StringProperty()
	text = db.StringProperty(multiline=True) # might consider db.TextProperty in the future


class User(db.Model):
    username = db.StringProperty()
    password = db.StringProperty() # might consider db.TextProperty in the future
