from mongoalchemy.document import Document, DocumentField
from mongoalchemy.fields import StringField, DateTimeField

class User(Document):
    username = StringField()
    password = StringField()

class File(Document):
    filename = StringField()
    filepath = StringField()
    author = DocumentField(User)
    title = StringField()
    caption = StringField()
    date = DateTimeField()