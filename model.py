from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session


engine = create_engine("sqlite:///ratings.db", echo = False)
session = scoped_session(sessionmaker(bind = engine, autocommit = False, autoflush = False)) # scoped_session is being used to guarantee thread-safety for multiple users accessing this same app

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User (Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	email = Column(String(64), nullable = True)
	password = Column(String(64), nullable = True)
	age = Column(Integer, nullable = True)
	zipcode = Column(String(15), nullable = True)

	# don't use init function because SQLAlchemy will also use this when creating a new object after pulling a row from the DB
	# def __init__(self, age, zipcode, email = None, password = None):
	# 	self.email = email
	# 	self.password = password
	# 	self.age = age
	# 	self.zipcode = zipcode

class Movie (Base):
	__tablename__ = "movies"

	id = Column(Integer, primary_key = True)
	name = Column(String(128))
	released_at = Column(String(128), nullable = True)
	imdb_url = Column(String(128), nullable = True)

	rating = relationship("Rating", backref="movie") # establishes a connection between Movies and Ratings class, use "movie" as the attribute name when referring to a Movies object from a Ratings object

	# def __init__(self, name, released_at = None, imdb_url = None):
	# 	self.name = name
	# 	self.released_at = released_at
	# 	self.imdb_url = imdb_url
  
class Rating (Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key = True)
	movie_id = Column(Integer, ForeignKey('movies.id'))
	user_id = Column(Integer, ForeignKey('users.id'))
	rating = Column(Integer)

	user = relationship("User", backref=backref("ratings", order_by=id)) # establishes connection to Users class based on foreign key to users.id indicated above, use "ratings" when referring to it from a User object. backref() is a function to use when wanting to pass additional parameter for SQL query to SQLAlchemy, here passing in paramter for query to use an "ORDER BY id" clause

	# def __init__(self, movie_id, user_id, rating):
	# 	self.movie_id = movie_id
	# 	self.user_id = user_id
	# 	self.rating = rating

### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__": # calls main function if we were to run this model.py file directly (vs. importing into another Python file)
    main()
