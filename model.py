from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here
class User (Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	email = Column(String(64), nullable = True)
	password = Column(String(64), nullable = True)
	age = Column(Integer, nullable = True)
	zipcode = Column(String(15), nullable = True)

	# don't need init function because we're inheriting from Base and not doing any calculations here anyway
	def __init__(self, age, zipcode, email = None, password = None):
		self.email = email
		self.password = password
		self.age = age
		self.zipcode = zipcode

class Movies (Base):
	__tablename__ = "movies"

	id = Column(Integer, primary_key = True)
	name = Column(String(128))
	released_at = Column(String(128), nullable = True)
	imdb_url = Column(String(128), nullable = True)

	def __init__(self, name, released_at = None, imdb_url = None):
		self.name = name
		self.released_at = released_at
		self.imdb_url = imdb_url
  
class Ratings (Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key = True)
	movie_id = Column(Integer)
	user_id = Column(Integer)
	rating = Column(Integer)

	def __init__(self, movie_id, user_id, rating):
		self.movie_id = movie_id
		self.user_id = user_id
		self.rating = rating

### End class declarations
def connect():
	global ENGINE
	global Session

	ENGINE = create_engine("sqlite:///ratings.db", echo = False)
	Session = sessionmaker(bind = ENGINE)

	return Session() # return an instance of one connection to the session


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
