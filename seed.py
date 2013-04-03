import model
import csv
from datetime import datetime # this is to avoid having to call datetime.datetime.strptime below but that works too


#for bulk uploading data from files

def load_users(session):
    # use u.user
    with open('seed_data/u.user') as csvfile:   
        # dialect = csv.Sniffer().sniff(csvfile.read(1024))
        # csvfile.seek(0)
        userlist = csv.reader(csvfile, delimiter = "|")
        for row in userlist:
            new_user = model.User(age=row[1], zipcode=row[4])
            new_user.id = row[0]
            session.add(new_user)


def load_movies(session):
    # use u.item
    count = 0
    with open('seed_data/u.item') as csvfile:
        itemlist = csv.reader(csvfile, delimiter = "|")
        for row in itemlist:
            # print row[2] #released_at for model.py; string form
            # print datetime.strptime(row[2], "%d-%b-%Y")

            row[1] = row[1].decode("latin-1") # change names from latin-1 encoding to unicode strings for sqlite3 db
            if row[2]: # to account for any movies that don't have a released_at listed, else get ValueError: time data '' does not match format '%d-%b-%Y'
                row[2] = datetime.strptime(row[2], "%d-%b-%Y") # converts 01-Jan-1995 to 1995-01-01 00:00:00 to store in DB as a datetime format for the released_at column
            new_movie = model.Movie(name=row[1], released_at=row[2], imdb_url=row[4])
            new_movie.id = row[0]
            session.add(new_movie)
            count += 1
            print "Movie #", count


def load_ratings(session):
    # use u.data
    count = 0
    with open('seed_data/u.data') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024)) # or could have used /t to indicate tab as a delimiter
        csvfile.seek(0)
        itemlist = csv.reader(csvfile, dialect)
        for row in itemlist:
            new_rating = model.Rating(movie_id=row[1], user_id=row[0], rating=row[2])
            session.add(new_rating)
            count += 1
            print "Rating #", count 

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    #load_users(session)
    load_movies(session)
    #load_ratings(session)
    
    session.commit() # much much faster to commit all the new rows all at once

if __name__ == "__main__":
    s= model.connect()
    main(s)
