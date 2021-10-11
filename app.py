# from logging import debug
import os
from flask import (
  Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists('env.py'):
  import env


# _____ CONFIGURATION _____ #


app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


# _____ INDEX _____ #


@app.route('/')
def index():
  return render_template('index.html')


# _____ CURRENT AUCTION _____ #


@app.route('/auction')
def auction():
  items = mongo.db.items.find()
  return render_template('auction.html', items=items)


# _____ REGISTER _____ #


@app.route('/register', methods=["GET", "POST"])
def register():
  if request.method == "POST":
    # Check if the email exists already in the database
    existing_user = mongo.db.users.find_one(
      {"email": request.form.get("email").lower()}
    )
    if existing_user:
      flash("Email already registered")
      return redirect(url_for("register"))

    register = {
      "email": request.form.get("email").lower(),
      "password": generate_password_hash(request.form.get("password")),
      "title": request.form.get("title").lower(),
      "first_name": request.form.get("first_name").lower(),
      "last_name": request.form.get("last_name").lower(),
      "newsletter": request.form.get("newsletter")
    }
    mongo.db.users.insert_one(register)

    # Put the new user into "session" cookie
    session["user"] = request.form.get("email").lower()
    flash("Registration Successful, Welcome!")
    return redirect(url_for("profile", username=session["user"]))
  return render_template('register.html')


# _____ LOGIN _____ #


@app.route('/login', methods=["GET", "POST"])
def login():
  if request.method == "POST":
    # Check if the email is already in the database
    existing_user = mongo.db.users.find_one(
      {"email": request.form.get("email").lower()}
    )

    if existing_user:
      # Check if the hashed password matches the user input
      if check_password_hash(
        existing_user["password"], request.form.get("password")):
          session["user"] = request.form.get("email").lower()
          flash("Welcome, {}".format(request.form.get("email")))
          return redirect(url_for("profile", email=session["user"]))
      else:
        # Invalid password
        flash("Incorrect email and/or password.")
        return redirect(url_for("login"))
    else:
      # Email not registered
      flash("Incorrect email and/or password.")
      return redirect(url_for("login"))
  return render_template('login.html')


# _____ PROFILE _____ #


@app.route('/profile/<id>', methods=["GET", "POST"])
def profile(email):
  # Grab the session's user email from database
  email = mongo.db.users.find_one(
    {"email": session["user"]})["email"]

  if session["user"]:
    return render_template('profile.html', email=email)

  return redirect(url_for("login"))


# _____ LOCAL SERVER _____ #


if __name__ == '__main__':
  app.run(host=os.environ.get('IP'),
          port=int(os.environ.get('PORT')),
          debug=True)