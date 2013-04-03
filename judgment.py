from flask import Flask, render_template, redirect, request
import model
import urllib # used for URL encoding


app = Flask(__name__)


@app.route("/")
def index():
	user_list = model.session.query(model.User).limit(5).all()
	return render_template("user_list.html", users = user_list)

@app.route("/ratings/<id>")
def show_ratings(id=None):
	# command that grabs movies and ratings for that user
	ratings_list = model.session.query(model.Ratings).filter_by(user_id=id).limit(5).all()

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

	new_user = model.User(email=form_email, password=form_password, age=form_age, zipcode=form_zipcode) 

	model.session.add(new_user)
	model.session.commit()
	return redirect("/")

if __name__ == "__main__":
	app.run(debug = True)


