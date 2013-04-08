from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import correlation

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

	# function to get Pearson correlation between two users' ratings for the same movies
    def similarity(self, other):
        u_ratings = {}
        paired_ratings = []

        for r in self.ratings: # for each rating of current user, add that rating object to the dictionary with the movie id as the key
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id) # look up the second user's movie id as a key in the dictionary, get out the first user's rating object for that movie
            if u_r:
                paired_ratings.append((u_r.rating, r.rating)) # add first user's rating and second user's rating for the same movie as a tuple to the list paired_ratings

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    # function to product a predicted rating on a specific movie for the user based on the top most similar user to this one
    def predict_rating(self, movie):
        ratings = self.ratings # create a list called ratings of all of this user's movie ratings
        other_ratings = movie.rating # create a list of all other ratings for the given movie
        # other_users =[ r.user for r in other_ratings] # create a list of all the users that have rated the given movie
        
        similarities = [(self.similarity(r.user), r) for r in other_ratings] # create a list of tuples, first item in tuple is similarity coefficient, second item in tuple is the other user's rating object for the given movie
        similarities.sort(reverse = True) # sort the list of tuples from highest correlation coefficient to lowest
        # top_user = similarities[0] # grab the user with the highest correlation coefficient
        # commenting this section out because now directly adding other user's rating to the similarities list
        #Find the top_user's rating for the given movie in the list of other_ratings for the given movie. 
        # matched_rating = None
        # for rating in other_ratings: 
        #     if rating.user_id == top_user[1].id:
        #         matched_rating = rating # Assign the top user's rating for that movie to the variable matched_rating
        #         break # stop searching through all the other_ratings once you've found the one made by the top_user

        # return top_user[0] * matched_rating.rating # multiple similarity coefficient by rating to give the predicted rating 

        # return top_user[0] * top_user[1].rating # return similarity coefficient multipled by top user's rating for the given movie

        # calculate a weighted mean to return as the predicted rating
        similarities = [ sim for sim in similarities if sim[0] > 0]
        if not similarities:
            return None
        numerator = sum([ r.rating * similarity for similarity, r in similarities])
        denominator = sum([ similarity[0] for similarity in similarities])

        return numerator/denominator
        


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
