from flask import Flask, flash, render_template, redirect, request, session, url_for
import model
import urllib # used for URL encoding


app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route("/")
def index():
	user_list = model.session.query(model.User).limit(5).all()
	return render_template("user_list.html", users = user_list)

@app.route("/ratings/<id>")
def show_ratings(id=None):
	# command that grabs movies and ratings for that user
	ratings_list = model.session.query(model.Rating).filter_by(user_id=id).limit(5).all()

	return render_template("user_ratings.html", ratings = ratings_list)

@app.route("/create_user")
def create_user():
	return render_template("create_user.html")

@app.route("/save_user", methods=["POST"])
def save_user():

	form_email = urllib.quote(request.form['email'])
	form_password = urllib.quote(request.form['password'])
	form_age = urllib.quote(request.form['age'])
	form_zipcode = urllib.quote(request.form['zipcode'])

	if form_email and form_password:
		new_user = model.User(email=form_email, password=form_password, age=form_age, zipcode=form_zipcode) 
		model.session.add(new_user)
		model.session.commit()
		return redirect("/")
	else:
		flash('Please enter a valid email address and password.')
		return redirect("/create_user")

@app.route("/login", methods=['GET'])
def login():
	return render_template("login.html")

@app.route("/validate_login", methods=["POST"])
def validate_login():
	form_email = urllib.quote(request.form['email'])
	form_password = urllib.quote(request.form['password'])

	#form_email and form_password must both exist and match in db for row to be an object. Row is the entire row from the users table, including the id
	row = model.session.query(model.User).filter_by(email=form_email, password=form_password).first()

	if row: 		
		session['email'] = request.form['email']
		session['user_id'] = row.id
		flash('Logged in as: ' + session['email'])
		return redirect("/")		
	else:
		flash('Please enter a valid email address and password.')
		return redirect("/login") 

@app.route("/logout")
def logout():
	session.pop('email', None)
	session.pop('user_id', None)
	flash('You have logged out.')
	return redirect(url_for('index'))

@app.route("/movies/<id>") #/movies/movie_id
def movies(id=None):
	#get the movie by movie_id
	movie_object = model.session.query(model.Movie).filter_by(id=id).first() #.first returns the first matching instance. This is sufficient because we are only looking up one movie.

	rated_movie = "" # declare to this be empty to still be able to pass into render_template without an error

	# if a user is logged in, run query to get user's rating for the movie in question.
	if "user_id" in session:
		rated_movie = model.session.query(model.Rating).filter(model.Rating.user_id==session['user_id'],model.Rating.movie_id==id).first()

	return render_template("movie.html", movie = movie_object, rated_movie = rated_movie) # pass in movie_object to the movie.html template as a parameter called, "movie"

@app.route("/my_ratings") 
def my_ratings():
	my_ratings = model.session.query(model.Rating).filter_by(user_id=session['user_id']).all() #contains all the rows of all ratings logged by  the user. The rows also contain movie id and info.
	return render_template("my_ratings.html", my_rat = my_ratings) #pass in my_ratings to the my_ratings.html template

@app.route("/movie_search_results", methods = ['POST'])
def movie_search_results():	
	form_movie = request.form['movie_title']
	movies = model.session.query(model.Movie).filter(model.Movie.name.like("%"+ form_movie + "%")).all()
	
	ratings_dict = {} # declare this so can pass it into render_template even if doesn't exist

	# grab ratings for movies in search results by logged in user if there is a user logged in
	if "user_id" in session:
		list_ids = []
		for movie in movies:
			list_ids.append(movie.id) # makes a list of movie ids from search results

		# querying for ratings objects given the logged-in user's ID and the movies that will be displayed on this search results page
		user_ratings = model.session.query(model.Rating).filter(model.Rating.user_id==session['user_id'],model.Rating.movie_id.in_(list_ids)).all()

		for rating in user_ratings:
			ratings_dict[rating.movie_id] = rating.rating # add key-values into dict with movie_id as key and rating as value

	return render_template("search_results.html", movies = movies, ratings_dict = ratings_dict)

if __name__ == "__main__":
	app.run(debug = True)


