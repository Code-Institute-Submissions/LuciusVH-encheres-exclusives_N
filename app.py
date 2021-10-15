# from logging import debug
import os
from flask import (
  Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
# from werkzeug.datastructures import ContentSecurityPolicy
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
@app.route('/index')
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

    newsletter = "yes" if request.form.get("newsletter") else "no"
    register = {
      "email": request.form.get("email").lower(),
      "password": generate_password_hash(request.form.get("password")),
      "title": request.form.get("title").lower(),
      "first_name": request.form.get("first_name").lower(),
      "last_name": request.form.get("last_name").lower(),
      "newsletter": newsletter
    }
    mongo.db.users.insert_one(register)

    # Put the new user into "session" cookie
    user_data = mongo.db.users.find_one(
      {"email": request.form.get("email").lower()}
    )
    session["user"] = str(user_data["_id"])
    flash("Registration Successful, Welcome!")
    return redirect(url_for("profile", user_id=session["user"]))
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
          session["user"] = str(existing_user["_id"])
          flash("Welcome, {}".format(request.form.get("email")))
          return redirect(url_for("profile", user_id=session["user"]))
      else:
        # Invalid password
        flash("Incorrect email and/or password.")
        return redirect(url_for("login"))
    else:
      # Email not registered
      flash("Incorrect email and/or password.")
      return redirect(url_for("login"))
  return render_template('login.html')

# _____ LOGOUT _____ #

@app.route('/logout')
def logout():
  # Remove the user from the session cookie
  # flash("You have been logged out")
  session.pop("user")
  return redirect(url_for("login"))

# _____ PROFILE _____ #

@app.route('/profile/<user_id>', methods=["GET", "POST"])
def profile(user_id):
  # Grab the session's user details from database
  user = mongo.db.users.find_one(
    {"_id": ObjectId(session["user"])}
  )

  if session["user"]:
    return render_template('profile.html', 
                            user_id=user["_id"], 
                            email=user["email"], 
                            title=user["title"], 
                            first_name=user["first_name"], 
                            last_name=user["last_name"])

  return redirect(url_for("login"))


# _____ EDIT PROFILE _____ #

@app.route('/edit_profile/<user_id>', methods=["GET", "POST"])
def edit_profile(user_id):
  # Grab the session's user details from database
  user = mongo.db.users.find_one(
    {"_id": ObjectId(user_id)} 
  )

  if request.method == "POST":
    newsletter = "yes" if request.form.get("newsletter") else "no"
    updated_profile = { 
      "email": request.form.get("email").lower(),
      "title": request.form.get("title").lower(),
      "first_name": request.form.get("first_name").lower(),
      "last_name": request.form.get("last_name").lower(),
      "newsletter": newsletter 
    }
    
    mongo.db.users.update_one(
      {"_id": ObjectId(user_id)},
      {"$set": updated_profile}) 

    # Check if the password field has been updated too
    updated_password = {}
    if len(request.form.get("password")) != 0:
      updated_password_data = {
        "password": generate_password_hash(request.form.get("password"))
      }
      updated_password = updated_password_data

    mongo.db.users.update_one(
      {"_id": ObjectId(user_id)},
      {"$set": updated_password})

    flash("Profile Updated")
  
  return render_template('edit_profile.html', 
                          user_id=user["_id"], 
                          email=user["email"], 
                          title=user["title"], 
                          first_name=user["first_name"], 
                          last_name=user["last_name"])


# _____ DELETE PROFILE _____ #

@app.route('/delete_profile/<user_id>')
def delete_profile(user_id):
  mongo.db.users.remove({'_id': ObjectId(user_id)})
  return redirect(url_for('index'))


# _____ LOCAL SERVER _____ #

if __name__ == '__main__':
  app.run(host=os.environ.get('IP'),
          port=int(os.environ.get('PORT')),
          debug=True)