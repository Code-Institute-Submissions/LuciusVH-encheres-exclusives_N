import os
from flask import (Flask, flash, render_template,
   redirect, request, session, url_for, jsonify)
from flask.scaffold import F
from flask_pymongo import PyMongo
import json
from bson.objectid import ObjectId
# from bson import json_util
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from operator import itemgetter
if os.path.exists('env.py'):
  import env


# _____ CONFIGURATION _____ #

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


# _____ BASE _____ #

"""
  Convert BSON data, coming from MongoDB, to JSON
  Code snippet found on https://stackoverflow.com/a/65538552

"""

class MyEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, ObjectId):
      return str(obj)
    elif isinstance(obj, datetime):
      return str(obj)
    return super(MyEncoder, self).default(obj)

app.json_encoder = MyEncoder


@app.context_processor
def auctions_dispatch():

  """
  Maintain the current_auctions & upcoming_auctions lists up-to-date.

  """
  auctions = list(mongo.db.auctions.find().sort('date_start', 1))
  current_auctions = []
  upcoming_auctions = []
  current_auctions.clear()
  upcoming_auctions.clear()
  now = datetime.today()

  for auction in auctions:
    if auction["date_start"] <= now and now <= auction["date_end"]:
      # Add the auction to the current_auctions list
      current_auctions.append(auction)
    elif auction["date_start"] <= now and now >= auction["date_end"]:
      # Updates the auction dates by incrementing date_start & date_end by as many weeks as there are auction categories
      updated_dates = {
        "date_start" : auction['date_start'] + timedelta(
          days=7*mongo.db.auctions.count_documents({})),
        "date_end" : auction['date_end'] + timedelta(
          days=7*mongo.db.auctions.count_documents({}))
      }
      updated_auction = mongo.db.auctions.update_one(
        {'_id' : auction['_id'] },
        { "$set": updated_dates}
      )
      # Add the newly updated auction to the upcoming_auctions list
      upcoming_auctions.append(updated_auction)
    else:
      # Add the auction to the upcoming_auctions list
      upcoming_auctions.append(auction)

  return dict(current_auctions=current_auctions, upcoming_auctions=upcoming_auctions)


"""
  Access and formate nicely the end date of a running auction.
  Code snippet written by Sean, tutor help.

"""
@app.template_filter()
def date_end(dttm):
  t = dttm['date_end']
  t = t.strftime('%B %d, %Y ― %H:%M')
  return t


# _____ INDEX _____ #

@app.route('/', methods=["GET", "POST"])
def index():
  auctions_dispatch()
  newest_auction = current_auctions[0]
  auction_category = newest_auction["category"]
  items = list(mongo.db.items.find({"category": auction_category}))
  return render_template('index.html', newest_auction=newest_auction, items=items)


# _____ AUCTION _____ #

@app.route('/auction')
def auction():
  items = mongo.db.items.find()
  return render_template('auction.html', items=items)

# _____ PLACE BID _____ #

@app.route('/place_bid/<item_id>', methods=["GET", "POST"])
def place_bid(item_id):
  # Collect data from the user's input on the form to update the items collection
  if request.method == "POST":
    user_bid = int(request.form.get("user_bid"))
    item = mongo.db.items.find_one(
    {"_id": ObjectId(item_id)} 
  )
    starting_price = item['starting_price']
    actual_bid = item['actual_bid']
    # Check that the user's input is greater than actual_bid, if there's, or than the starting price otherwise
    if user_bid > int(actual_bid) > int(starting_price):
      bid_placed = {
        "actual_bid": user_bid,
        "actual_bidder": session["user"]
      }
      mongo.db.items.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": bid_placed})
      return redirect(url_for("index"))
    else:
      return redirect(url_for("index"))
  return render_template('index.html')


# _____ REGISTER _____ #

@app.route('/register', methods=["GET", "POST"])
def register():
  if request.method == "POST":
    # Check if the email exists already in the database
    existing_user = mongo.db.users.find_one(
      {"email": request.form.get("email").lower()}
    )
    if existing_user:
      flash("Email already registered", "error")
      return redirect(url_for("login"))

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
      # Check if the hashed password matches the user's input
      if check_password_hash(
        existing_user["password"], request.form.get("password")):
          session["user"] = str(existing_user["_id"])
          return redirect(url_for("profile", user_id=session["user"]))
      else:
        # Invalid password
        flash("Incorrect email and/or password", "error")
        return redirect(url_for("login"))
    else:
      # Email not registered
      flash("Incorrect email and/or password", "error")
      return redirect(url_for("login"))
  return render_template('login.html')

# _____ LOGOUT _____ #

@app.route('/logout')
def logout():
  # Remove the user from the session cookie
  session.pop("user")
  flash("You've been logged out. Come back soon!", "bye")
  return redirect(url_for("login"))

# _____ PROFILE _____ #

@app.route('/profile/<user_id>', methods=["GET", "POST"])
def profile(user_id):
  # Forbid access to non logged-in users
  if session:
    # Grab the session's user details from database
    user = mongo.db.users.find_one(
      {"_id": ObjectId(session["user"])}
    )
    # Retrieve the user's items to be sold
    user_items = list(mongo.db.items.find(
      {"created_by": session["user"]} 
    ))
    # Retrieve the different auctions categories
    categories = list(mongo.db.auctions.find().sort("category", 1))
    return render_template('profile.html', 
                            user=user,
                            user_items=user_items,
                            categories=categories)
  else:
    return redirect(url_for("login"))
  


# _____ EDIT PROFILE _____ #

@app.route('/edit_profile/<user_id>', methods=["GET", "POST"])
def edit_profile(user_id):
  # Forbid access to non logged-in users
  if not session:
    return redirect(url_for("login"))

  # Collect data from the user's inputs on the form to update the users collection
  elif request.method == "POST":
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
    flash("Profile Updated", "valid")
    return redirect(url_for('profile', user_id=user_id)) 

  #Forbid access to logged-in users who aren't the owner of the account
  elif session["user"] == user_id:
    # Grab the session's user details from database
    user = mongo.db.users.find_one(
      {"_id": ObjectId(user_id)} 
    )
    return render_template('edit_profile.html', user=user)
  else:
    flash("This is not your profile to edit...", "error")
    return redirect(url_for('profile', user_id=user_id))


# _____ DELETE PROFILE _____ #

@app.route('/delete_profile/<user_id>')
def delete_profile(user_id):
  # Forbid access to non logged-in users
  if session:
    # Forbid access to logged-in users who aren't the owner of the account
    if session["user"] == user_id:
      mongo.db.users.remove({'_id': ObjectId(user_id)})
      session.pop("user")
      flash("Account Deleted", "deleted")
      return redirect(url_for('index'))
    else:
      flash("This is not your profile to delete...", "error")
      return redirect(url_for('profile', user_id=session["user"]))
  else:
    return redirect(url_for("login"))


# _____ ADD A LOT _____ #

@app.route('/add_lot', methods=["GET", "POST"])
def add_lot():
  # Collect data from the user's inputs on the form to insert the entry on the items collection
  if request.method == "POST":
    starting_price = int(request.form.get("addlot-estimatedprice")) // 10
    new_item = {
      "category": request.form.get("addlot-category"),
      "title": request.form.get("addlot-title").title(),
      "brand_artist": request.form.get("addlot-artistbrand").title(),
      "estimated_price": int(request.form.get("addlot-estimatedprice")),
      "starting_price": starting_price,
      "image_url": request.form.get("addlot-imageurl"),
      "created_by": session["user"],
      "actual_bid": 0
    }
    mongo.db.items.insert_one(new_item)
    flash("Your item has been added to the auction", "valid")
    return redirect(url_for("profile", user_id=session["user"]))
  return render_template('profile.html', user_id=session["user"])


# _____ DELETE ITEM _____ #

@app.route('/delete_item/<item_id>')
def delete_item(item_id):
  # Forbid access to non logged-in users
  if session:
    users_item = mongo.db.items.find_one({'_id': ObjectId(item_id)})
    print(users_item)
    user_id = users_item["created_by"]
    # Forbid access to logged-in users who aren't the owner of the item
    if session["user"] == user_id:
      mongo.db.items.remove({'_id': ObjectId(item_id)})
      flash("Your item has been deleted", "deleted")
      return redirect(url_for('profile', user_id=user_id))
    else:
      flash("This is not your item to delete...", "error")
      return redirect(url_for('profile', user_id=user_id))
  else:
    return redirect(url_for("login"))

# _____ NEWSLETTER _____ #
@app.route('/newsletter', methods=["GET", "POST"])
def newsletter():
  # Collect data from the user's inputs on the form to insert the entry on the newsletter collection
  if request.method == "POST":
    existing_user = mongo.db.newsletter.find_one(
      {"email": request.form.get("email").lower()}
    )
    
    if existing_user:
      flash("Email already registered", "error")
      return redirect(url_for("index"))

    subscription = {
      "email": request.form.get("email").lower(),
      "title": request.form.get("title").lower(),
      "first_name": request.form.get("first_name").lower(),
      "last_name": request.form.get("last_name").lower(),
    }
    mongo.db.newsletter.insert_one(subscription)
    flash("Thank you, we stay in touch!", "valid")
    return redirect(url_for("index"))
  return render_template("index.html")

# _____ LOCAL SERVER _____ #

if __name__ == '__main__':
  app.run(host=os.environ.get('IP'),
          port=int(os.environ.get('PORT')),
          debug=True)