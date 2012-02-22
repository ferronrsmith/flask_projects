from photolog import db

# documents
class User(db.Document):
    username = db.StringField()
    password = db.StringField()

class File(db.Document):
    filename = db.StringField()
    filepath = db.StringField()
    fileabslink = db.StringField()
    author = db.DocumentField(User)
    title = db.StringField()
    caption = db.StringField()
    date = db.DateTimeField()