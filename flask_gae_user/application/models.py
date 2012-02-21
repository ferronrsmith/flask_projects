from google.appengine.ext import db

class Blog(db.Model):
	title = db.StringProperty(multiline=False)
	text = db.StringProperty(multiline=True) # might consider db.TextProperty in the future