import os
from flask import (Flask, flash, render_template,
  redirect, request, session, url_for, Markup)
from flask_pymongo import PyMongo
import json
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import yagmail
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


"""
  Functions determining if an auction is running or is upcoming
  Code snippet written with the help of my mentor

"""
def is_auction_running(auction):
  now = datetime.today()
  if auction["date_start"] <= now and now <= auction["date_end"]:
    return True
  else:
    return False

def has_auction_ended(auction):
  now = datetime.today()
  if now >= auction["date_end"]:
    return True
  else:
    return False


@app.context_processor
def auctions_dispatch():
  """
  Maintain the current_auctions & upcoming_auctions lists up-to-date.
  Maintain the collections lots & lots_sold up-to-date.

  """
  auctions = list(mongo.db.auctions.find().sort('date_start', 1))
  current_auctions = []
  upcoming_auctions = []

  for auction in auctions:

    if is_auction_running(auction):
      # Add the auction to the current_auctions list
      current_auctions.append(auction)
    elif has_auction_ended(auction):
      # Update the auction dates by incrementing date_start & date_end by as many weeks as there are auction categories
      updated_data = {
          "date_start": auction['date_start'] + timedelta(
          days=7*mongo.db.auctions.count_documents({})),
          "date_end": auction['date_end'] + timedelta(
          days=7*mongo.db.auctions.count_documents({})),
      }
      mongo.db.auctions.update_one(
        {'_id' : auction['_id'] },
        { "$set": updated_data}
      )

      # Since this auction is over, transfer the sold lots from the lots collection to the lots_sold collection
      all_lots_from_this_category = list(mongo.db.lots.find({"category": auction['category']}))
      print(all_lots_from_this_category)
      for lot in all_lots_from_this_category:
        # Verify if the reserve price has been met, to declare the lot sold
        if lot['highest_bid'] > lot ['reserve_price']:
          lot_sold_data = {
            "category": lot['category'],
            "title": lot['title'],
            "brand_artist": lot['brand_artist'],
            "final_bidder": lot['actual_bidder'],
            "final_bid": lot['highest_bid'],
            "final_bid_time": lot['bid_time'],
            "estimated_price": lot['estimated_price'],
            "image_url": lot['image_url'],
            "bids_history": list(lot['previous_bids_details']),
            "sold_created_by": lot['created_by'],
            "creation_time": lot['creation_time'],
          }
          mongo.db.lots_sold.insert_one(lot_sold_data)
          mongo.db.lots.delete_one({'_id': lot['_id']})
        # And reset the lots not sold (with no bids or when the reserve price has not been reached)
        else:
            lot_not_sold = {
                "highest_bid": 0,
                "actual_bidder": None,
                "previous_bids_details": None
            }
            mongo.db.lots.update_one(
                {'id': lot['_id']},
                {'$set': lot_not_sold})

      # Add the newly updated auction to the upcoming_auctions list
      upcoming_auctions.append(auction)
    else: 
      upcoming_auctions.append(auction)

  # Check which two auction categories are currently running
  running_categories = []
  for auction in current_auctions:
    running_categories.append(auction["category"])

  return dict(current_auctions=current_auctions, upcoming_auctions=upcoming_auctions, running_categories=running_categories)


"""
  Access and formate nicely the dates of an auction, or the prices displayed.

"""
@app.template_filter()
def date_start(dttm):
  t = dttm['date_start']
  t = t.strftime('%B %d, %Y ― %H:%M')
  return t

@app.template_filter()
def price_format(price):
  return format(int(price), ',d')

# Code snippet written by Sean, tutor help.
@app.template_filter()
def date_end(dttm):
  t = dttm['date_end']
  t = t.strftime('%B %d, %Y ― %H:%M')
  return t


# _____ INDEX _____ #

@app.route('/', methods=["GET"])
def index():
  dispatch_data = auctions_dispatch()
  # Isolate the newest auction, its data & its lots
  newest_auction = dispatch_data["current_auctions"][0]
  auction_category = newest_auction["category"]
  lots = list(mongo.db.lots.find({"category": auction_category}))
  if session:
    # Grab the session's user details from database
    user = mongo.db.users.find_one(
      {"_id": ObjectId(session["user"])}
    )
    # Retrieve the user's lots to be sold
    user_lots = list(mongo.db.lots.find({"created_by": session["user"]}))
    # Retrieve the different auctions categories
    categories = list(mongo.db.auctions.find().sort("category", 1))
    return render_template('index.html',
                        newest_auction=newest_auction,
                        lots=lots,
                        user=user,
                        user_lots=user_lots,
                        categories=categories)
  else:
    return render_template('index.html',
                            newest_auction=newest_auction,
                            lots=lots)



# _____ AUCTION _____ #

@app.route('/auction/<category>', methods=["GET"])
def auction(category):
  # Retrieve the auction's details
  auction = mongo.db.auctions.find_one({"category": category})
  auction_running = is_auction_running(auction)
  # Retrieve the lots belonging to the chosen category
  lots = list(mongo.db.lots.find({"category": category}))
  if session:
    # Grab the session's user details from database
    user = mongo.db.users.find_one(
      {"_id": ObjectId(session["user"])}
    )
    # Retrieve the user's lots to be sold
    user_lots = list(mongo.db.lots.find({"created_by": session["user"]}))
    # Retrieve the different auctions categories
    categories = list(mongo.db.auctions.find().sort("category", 1))
    return render_template('auction.html',
                          auction=auction,
                          lots=lots,
                          user=user,
                          user_lots=user_lots,
                          categories=categories,
                          auction_running=auction_running)
  else:
    return render_template('auction.html',
                            auction=auction,
                            lots=lots,
                            auction_running = auction_running)


# _____ PLACE BID _____ #

@app.route('/place_bid/<lot_id>', methods=["GET", "POST"])
def place_bid(lot_id):
  # Collect data from the user's input on the form to update the lots collection
  if request.method == "POST":
    user_bid = int(request.form.get("user_bid"))
    try:
      lot = mongo.db.lots.find_one({"_id": ObjectId(lot_id)})
      starting_price = int(lot['starting_price'])
      highest_bid = int(lot['highest_bid'])

      # Check that the user's input is greater than highest_bid, if there's, or than the starting price otherwise
      if user_bid > highest_bid and user_bid > starting_price:
        # Retrieve the data of the soon-to-be previous bid and store it under "previous_bids_details"
        bid_placed = {
          "highest_bid": user_bid,
          "actual_bidder": session["user"],
          "bid_time": datetime.now()
        }
        if highest_bid != 0:
          actual_bidder = lot['actual_bidder']
          bid_time = lot['bid_time']
          previous_bid = {
          "previous_bids_details" : {
              "$each": [
                {
                  "previous_bidder": actual_bidder,
                  "previous_bid": highest_bid,
                  "previous_bid_time": bid_time
                }
              ]
            }
          }
          mongo.db.lots.update_one(
            {"_id": ObjectId(lot_id)},
            {"$set": bid_placed, "$push": previous_bid}
          )
        else:
          mongo.db.lots.update_one(
            {"_id": ObjectId(lot_id)},
            {"$set": bid_placed}
          )
        return redirect(url_for("index"))
      else:
        return redirect(url_for("index"))
    except:
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

    newsletter = True if request.form.get("newsletter") else False
    register = {
      "email": request.form.get("email").lower(),
      "password": generate_password_hash(request.form.get("password")),
      "title": request.form.get("title").lower(),
      "first_name": request.form.get("first_name").lower(),
      "last_name": request.form.get("last_name").lower(),
      "newsletter_subscribed": newsletter,
      "registration_time": datetime.now()
    }
    mongo.db.users.insert_one(register)

    # Put the new user into "session" cookie
    user_data = mongo.db.users.find_one(
      {"email": request.form.get("email").lower()}
    )
    session["user"] = str(user_data["_id"])
    return redirect(url_for("profile"))
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
          return redirect(url_for("profile"))
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


# _____ HOW DOES IT WORK REDIRECT LINK _____ #

@app.route('/howdoesitwork')
def howdoesitwork():
  return redirect(url_for('about', _anchor='howdoesitwork'))


# _____ PROFILE _____ #

@app.route('/profile', methods=["GET", "POST"])
def profile():
  # Forbid access to non logged-in users
  if session:
    # Grab the session's user details from database
    user = mongo.db.users.find_one(
      {"_id": ObjectId(session["user"])}
    )
    # Retrieve lots for which the user holds the highest bid or has bid before but is now outbidden
    user_bids = list(mongo.db.lots.find(
      {"$or": [{"actual_bidder": session["user"]},
      {"previous_bids_details.previous_bidder": session["user"]}]}
    ))
    # Retrieve the user's lots to be sold
    user_lots = list(mongo.db.lots.find(
      {"created_by": session["user"]}
    ))
    # Retrieve the sold lots
    lots_sold = list(mongo.db.lots_sold.find(
      {"$or": [{"sold_created_by": session["user"]},
      {"final_bidder": session["user"]}]}
    ))
    # Retrieve the different auctions categories
    categories = list(mongo.db.auctions.find().sort("category", 1))
    return render_template('profile.html',
                            user=user,
                            user_bids=user_bids,
                            user_lots=user_lots,
                            lots_sold=lots_sold,
                            categories=categories)
  else:
    return redirect(url_for("login"))


# _____ EDIT PROFILE _____ #

@app.route('/edit_profile', methods=["GET", "POST"])
def edit_profile():
  # Forbid access to non logged-in users
  if not session:
    return redirect(url_for("login"))
  else:
    user = mongo.db.users.find_one(
        {"_id": ObjectId(session["user"])}
    )
    user_id = user["_id"]
    # Collect data from the user's inputs on the form to update the users collection
    if request.method == "POST":
      newsletter = True if request.form.get("newsletter") else False
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
      return redirect(url_for('profile'))
    return render_template('edit_profile.html', user=user)


# _____ DELETE PROFILE _____ #

@app.route('/delete_profile')
def delete_profile():
  # Forbid access to non logged-in users
  if session:
    # If the user's bid is the highest bid on some lots, delete this bid and switch back to the previous highest bidder
    current_bids = list(mongo.db.lots.find(
      {"actual_bidder": session["user"]}
    ))
    if current_bids:
      for lot in current_bids:
        actual_bidder = lot['previous_bids_details'][-1]['previous_bidder']
        bid_time = lot['previous_bids_details'][-1]['previous_bid_time']
        highest_bid = lot['previous_bids_details'][-1]['previous_bid']
        back_to_previous_bid = {
          "highest_bid": highest_bid,
          "actual_bidder": actual_bidder,
          "bid_time": bid_time
        }
        mongo.db.lots.update_one(
          {"_id": ObjectId(lot['_id'])},
          {"$set": back_to_previous_bid,
          "$pop": {"previous_bids_details": 1}}
        )
    # Delete the user's lots
    mongo.db.lots.delete_many({'created_by': session["user"]})
    # Delete the user's data
    mongo.db.users.delete_one({'_id': ObjectId(session["user"])})
    session.pop("user")
    flash("Account, lot(s) & bid(s) deleted", "deleted")
    return redirect(url_for('index'))
  else:
    return redirect(url_for("login"))


# _____ ADD A LOT _____ #

@app.route('/lot/add', methods=["GET", "POST"])
def add_lot():
  # Collect data from the user's inputs on the form to insert the entry on the lots collection
  if request.method == "POST":
    starting_price = int(request.form.get("addlot-estimatedprice")) // 10
    reserve_price = int(request.form.get("addlot-estimatedprice")) // 2
    new_lot = {
      "category": request.form.get("addlot-category"),
      "title": request.form.get("addlot-title").title(),
      "brand_artist": request.form.get("addlot-artistbrand").title(),
      "estimated_price": int(request.form.get("addlot-estimatedprice")),
      "starting_price": starting_price,
      "reserve_price": reserve_price,
      "highest_bid": 0,
      "image_url": request.form.get("addlot-imageurl"),
      "created_by": session["user"],
      "creation_time": datetime.now()
    }
    mongo.db.lots.insert_one(new_lot)
    flash("Your lot has been added to the auction", "valid")
    return redirect(url_for("profile"))
  return render_template('profile.html')


# _____ EDIT LOT _____ #

@app.route('/lot/<lot_id>/edit', methods=["GET", "POST"])
def edit_lot(lot_id):
  # Forbid access to non logged-in users
  if not session:
    return redirect(url_for("login"))
  else:
    # Collect data from the user's inputs on the form to update the users collection
    if request.method == "POST":
      updated_lot = {
        "category": request.form.get("editlot-category"),
        "title": request.form.get("editlot-title").title(),
        "brand_artist": request.form.get("editlot-artistbrand").title(),
        "image_url": request.form.get("editlot-imageurl")
      }
      mongo.db.lots.update_one(
        {"_id": ObjectId(lot_id)},
        {"$set": updated_lot})
      flash("Lot Updated", "valid")
      return redirect(url_for('profile'))
    return render_template('edit_lot.html', lot_id=lot_id)


# _____ DELETE LOT _____ #

@app.route('/lot/<lot_id>/delete')
def delete_lot(lot_id):
  # Forbid access to non logged-in users
  if session:
    users_lot = mongo.db.lots.find_one({'_id': ObjectId(lot_id)})
    user_id = users_lot["created_by"]
    # Forbid access to logged-in users who aren't the owner of the lot
    if session["user"] == user_id:
      mongo.db.lots.delete_one({'_id': ObjectId(lot_id)})
      flash("Your lot has been deleted", "deleted")
      return redirect(url_for('profile'))
    else:
      flash("This is not your lot to delete...", "error")
      return redirect(url_for('profile'))
  else:
    return redirect(url_for("login"))


# _____ ABOUT _____ #

@app.route('/about')
def about():
  return render_template('about.html')

# _____ CONTACT _____ #

@app.route('/contact', methods=["GET", "POST"])
def contact():
  if request.method == "POST":
    try:
      user_title = request.form.get("title")
      user_fname = request.form.get("first_name")
      user_lname = request.form.get("last_name")
      user_email = request.form.get("email")
      user_message = request.form.get("message")

      body = [
        f"<h3>You have received a message from {user_title} {user_fname} {user_lname}!</h3>",
        "<p>Here it is:</p>",
        f"<p>{user_message}</p>",
        f"<p>Answer them to: {user_email}</p>"
      ]

      yag = yagmail.SMTP(user='ms3.encheres.privees@gmail.com',
                        password=os.environ.get('EMAIL_PSWD'),
                        host='smtp.gmail.com')
      yag.send(
        subject=f"New message from {user_email}",
        contents=body
      )
      flash("Thank you for contacting us. We will get back to you shortly!", "valid")
    except:
      # If something goes wrong, invite the user to connect directly through mail
      message = Markup("Something went wrong... But you can write us as \
        <a href='mailto:ms3.encheres.privees@gmail.com'>\
        ms3.encheres.privees@gmail.com</a>!")
      flash(message, "error")
  return render_template('contact.html')


# _____ SEARCH _____ #

@app.route('/search', methods=["GET", "POST"])
def search():
  user_query = request.args.get('search-query')
  query = '"'+user_query+'"'
  lots = list(mongo.db.lots.find({"$text": {"$search": query}}))
  if session:
    # Grab the session's user details from database
    user = mongo.db.users.find_one(
      {"_id": ObjectId(session["user"])}
    )
    # Retrieve the user's lots to be sold
    user_lots = list(mongo.db.lots.find({"created_by": session["user"]}))
    # Retrieve the different auctions categories
    categories = list(mongo.db.auctions.find().sort("category", 1))
  else:
    return render_template('search_result.html',
                            lots=lots,
                            query=query)
  return render_template('search_result.html',
                          lots=lots,
                          query=query,
                          user=user,
                          user_lots=user_lots,
                          categories=categories)


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