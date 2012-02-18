from sqlalchemy import Column, Integer, String
from database import Base

class Blog(Base):
	__tablename__ = 'blog'
	id = Column(Integer, primary_key=True)
	title = Column(String(50), unique=False)
	text = Column(String(500), unique=False)

	def __init__ (self, title=None, text=None):
		self.title = title
		self.text = text
	


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50), unique=False)

    def __init__ (self, username=None, password=None):
        self.username = username
        self.password = password