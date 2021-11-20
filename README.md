# Third Milestone Project

<p align="center">
  <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/img/logo.svg" alt="Logo Enchères Exclusives"/>
</p>




Hi there and welcome! 

This is a website created as my third Milestone Project for the Full Stack Developer Course of [Code Institute](https://codeinstitute.net/), after completing the three first major modules : User Centric Front End Development, Interactive Frontend Development & Backend Development.  

You can find the deployed site [here](https://encheres-exclusives.herokuapp.com/).

> **NOTE:** The links included in this README will not automatically open in a new tab. Press CTRL+ click on the link to open the target in a new tab.



## Table of Content

1. [UX](https://github.com/LuciusVH/encheres-exclusives#ux)
   1. [Structure & Design](https://github.com/LuciusVH/encheres-exclusives#structure--design)
   2. [User Stories](https://github.com/LuciusVH/encheres-exclusives#user-stories)
2. [Features](https://github.com/LuciusVH/encheres-exclusives#features)
   1. [Existing Features](https://github.com/LuciusVH/encheres-exclusives#existing-features)
   2. [Features Left to Implement](https://github.com/LuciusVH/encheres-exclusives#features-left-to-implement)
3. [Technologies Used](https://github.com/LuciusVH/encheres-exclusives#technologies-used)
   1. [Web Technologies](https://github.com/LuciusVH/encheres-exclusives#web-technologies)
   2. [Developer tools](https://github.com/LuciusVH/encheres-exclusives#web-technologies)
4. [Testing](https://github.com/LuciusVH/encheres-exclusives#testing)
5. [Deployment](https://github.com/LuciusVH/encheres-exclusives#deployment)
6. [Credits](https://github.com/LuciusVH/encheres-exclusives#credits)
   1. [Content](https://github.com/LuciusVH/encheres-exclusives#content)
   2. [Media](https://github.com/LuciusVH/encheres-exclusives#media)
   3. [Acknowledgements](https://github.com/LuciusVH/encheres-exclusives#acknowledgements)




------
------

## UX

The world of auctions, known for selling famous artworks and extremely expensive items, is sometimes perceived as too closed or secret. It is a common misperception, turns out more than 90% of the auctions in the world are completely public and accessible to anyone who dares to cross the doorstep. This misconception is due to the fact that we only hear about the exceptional sales, proposing extraordinary lots, often reserved to already well known customers of the auction house hosting the event. *Enchères Exclusives* is a gateway to this realm, with the mission to make it more accessible, even from the comfort of your living room.

### 	Structure & Design

Designed as a multipage website, built with Flask, it allows the user to browse the different collections, create an account to bid on some lots of their liking, and sold some of their own. *Enchères Exclusives* also gives some precious information about the auction business, in order to familiarize the user and sort of demystify this world. 

I wanted the general design to stay clean and sleek, to allow the user to focus on the lots. The color panel is really neutral with Ghost White (#FAFAFF) and Gray80 (#CCCCCC) as background color when an element needs a bit more attention (like for a title banner). The global text color is also a gray, Gray20 (#333333). To highlight some elements, I used different shades of *Enchères Exclusives*'s indigo (#23448D). All contrast ratios were tested using [WebAIM.org contrast checker](https://webaim.org/resources/contrastchecker/). 

The <u>Home page</u> displays a hero image, the image being different depending on the viewport's width, to ensure a nice rendering on any screen. 

Below this, the latest auction is exposed, showing off the lots in a slider, each lot presented in a card. The number of cards depends on the width available: from 1 to 4. 

Next comes a section inviting the user to subscribe to the company's newsletter. 

Finally, a footer inviting the user to follow *Enchères Exclusives* on different social medias: Twitter, Facebook, Instagram, YouTube & Weibo. A discreet copyright mention is positioned under it, being aligned with the "Follow us" on desktop, or centered from a smaller screen. 

The navigation bar is pretty basic: the company's logo on the left, being a link to the homepage. Then 2 sections of links: on the left the company's related links with "Auctions", "About" & "Contact" ; On the right side, "Sign In / Sign Up" for a guest user, or "Profile / Log Out" for a registered user, and a "Search" bar. All these links collapse on tablet & phone screen, under a hamburger icon, right-positioned. It opens up a dropdown menu, displaying all the same links. Finally, from a computer, the logo gets reduced by half once the user starts scrolling down the page (while it's automatically set to 30px height on phone & tablet screens), giving more space to the content, and a shadow appears under the navbar to create a separation between the navbar and the rest of the website, both having the same background color. 

The <u>Auction link</u> dropdown menu is divided in two sections: the Current Auctions & the Upcoming Auctions. Each auction displays which category it belongs to (Art, Fashion & Jewels, Interior Design & Furniture, Watches, etc.) and either way when it starts if it's an upcoming auction, or when it ends if the auction is already running. 

The <u>About page</u> explains shortly how the app works and the auction process.

The <u>Contact page</u> is a simple contact form, allowing the user to get in touch with *Enchères Privées*. The form consists of a dropdown to select your appropriate title and 4 input fields (first name, last name, email & your message).

The <u>Register page</u> simply display a form with 4 input fields (email, password, first name & last name), a dropdown to select your appropriate title, a checkbox to receive the newsletter and a "Sign Up" button. Under that, a "Log In" link if the user misclicked and already is a member. Once validated, the user is redirected to the Profile page.

The <u>Login page</u> is also pretty simple: a form with 2 input fields (email & password), a "Log In" button. Under that, a "Sign Up" button as an invitation, if the user doesn't have an account already. Once validated, the user is redirected to the Profile page.

The <u>Profile page</u> display a personalized welcoming message followed by the user's data: full name (title, first name & last name), the email and "* * * * * *" as password. Below these are two links, allowing the user to *Edit* or *Delete* their profile. The links are discreet, as I did not want them to be so obviously visible as buttons or icons can be. Although it's a nice feature, I did not wanted it to take too much focus. 

Clicking on *Edit* leads the user to the <u>Edit Profile page</u>, of course, which is a copy of the Register page. The form is already populated with the user data registered in the database. As of now, I have an issue to prepopulate the title dropdown with the correct content (more on this in the [bugs](https://github.com/LuciusVH/encheres-exclusives#spotted-bugs--errors) section).

The *Delete* link opens up a Bootstrap "toast", playing the alert role (it is set up by aria attributes, for screen-readers): it asks the user for confirmation that they really want to delete their account, informing them that all data will be deleted with no possibility to cancel this action. 

Below this, the <u>My Bids</u> section. It consists of a slider, displaying the lots on which the user has bidden (whether they are still the highest bidder or not). It allows them to retrieve the lots for which they have an interest quickly. Under, <u>My Lots</u> display the user's own lots to be sold, in a second slider. They can be edited or deleted, but only until the auction in which they have been categorized begins. A link invites the user to get more familiar with the concept & working process of the app if needed, and finally a button opens up the <u>Add a lot modal</u>, allowing the user to submit their own lot to auction. The third and last section is available if the user has won any auction, or sold any lot. It also display the lots in a slider, and the action button this time links to the <u>Contact page</u>.

The <u>Auction page</u> displays all item of the auction's category, allowing the user to bid or not depending on whether the auction is running or not. Users can edit/delete their lots, depending on whether the auction is running or not.

### User stories

- As a buyer, I want to find new items for my collections. 
- As a user, I want to find information about the actual & upcoming sales. 
- As a seller & member, I want to resell some of my items. 
- As a buyer & member, I want to see my bids.
- As a buyer/seller, I want to find information about the whole process & how this works.
- As a seller & member, I want to be able to add my lot to be sold, edit or delete them.
- As a member, I want to be able to edit or delete my profile.
- As a new user, I want to be able to create an account.
- As a user, I want to subscribe to the newsletter.




## Features

### Existing Features

To see the whole list of features, please read the [Detailed Existing Features report](https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/).

### Features Left to Implement

- Password lost function & verification.
- Picture upload input & picture storage in db, instead of URL.
- Time display based on local timezone.
- Online payment, from the app.



## Technologies Used

### Web technologies

- [HTML](https://en.wikipedia.org/wiki/HTML)
- [CSS](https://en.wikipedia.org/wiki/CSS) 
- [JavaScript](https://www.javascript.com/)
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)

### Developer tools

- [Github](https://github.com/)
- [Heroku](https://www.heroku.com/)
- [Git](https://git-scm.com/) 
- [Visual Studio Code](https://code.visualstudio.com/)

- [Bootstrap 5.1](https://getbootstrap.com/docs/5.1/getting-started/introduction/)

- [Start Bootstrap](https://startbootstrap.com/)
  - The website basic [template](https://startbootstrap.com/template/shop-homepage) was downloaded from **Start Bootstrap** and customized.
- [Typora](https://typora.io/)
  - **Typora** was used to write this README file & its annexes.
- [Balsamiq](https://balsamiq.com/)
  - **Balsamiq** was used to create the wireframes. 
- [Inskcape](https://inkscape.org/)
  - **Inkscape** was used to create the SVG logo.
- [TinyPNG](https://tinypng.com/)
  - **TinyPNG** was used to compress all pictures, in order to reduce the loading time and improve UX. 
- [Favicon.io](https://favicon.io/)
  - **FavIcon** was used to create and implement the favicon. 



## Testing

The website has been tested automatically through W3C HTML & CSS validators, JavaScript was analyzed via JSHint, and the whole website with Lighthouse. 

### HTML Validator ([W3C](https://validator.w3.org/))

### CSS Validator ([W3C](https://jigsaw.w3.org/css-validator/validator.html))

### [JSHint](https://jshint.com/)


### Lighthouse

#### Link testing:



#### Spotted bugs & errors:

- **Edit page form "title" dropdown prepopulation**

  The form is supposed to be populated with all user's data. It works fine with other fields, but I can't seem to get this dropdown to display the correct title. The "*selected*" attribute is set to "Ms", as it is the first option in the list.

  <p align="center">
    <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/dropdown-prepopulated.png" alt="Bug with dropdown list selected option"/>
  </p>
  
  

<p align="center">
    <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/dropdown-prepopulated2.png" alt="Not matching the database data"/>
  </p>

<u>Solution:</u> N/A

- Grid issue when two sliders on the same page

  When two sliders from GlideJS are used on the same page, the grid of the 2nd slider seems off, as you can see in the picture below:

  <p align="center">
    <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/multiple-sliders.jpg" alt="Issue with the 2nd slider's grid when two sliders are on the same page"/>
  </p>

   <u>Solution:</u> To map the creation of each slider. This solution has been found in an [answer](https://github.com/glidejs/glide/issues/59#issuecomment-529124814) to this GlideJS known issue.

#### Tested user stories:

- As a buyer, I want to find new items for my collections. 

  *Enchères Privées provides the opportunity to buy incredible lots, no better place to expand your collections.*

- As a user, I want to find information about the actual & upcoming sales. 

  *The auctions, running and upcoming, are both displayed in the Auctions dropdown menu in the navbar.*

- As a seller & member, I want to resell some of my items. 

  *You can add your items through our Propose a lot modal, located on your Profile page.*

- As a buyer & member, I want to see my bids.

  *You can find all lots on which you have bidden on your Profile page.*

- As a buyer/seller, I want to find information about the whole process & how this works.

  *These information are available on the About page.*

- As a seller & member, I want to be able to add my lot to be sold, edit or delete them.

  *You can add, see, edit and delete them (CRUD) your lots through your Profile page.*

- As a member, I want to be able to edit or delete my profile.

  *You can edit or delete your profile and all your data through your Profile page.*

- As a new user, I want to be able to create an account.

  *The Register form is here for you!*

- As a user, I want to subscribe to the newsletter.

  *This is possible through the Newsletter form available on the Home page.*

## Deployment & cloning

You can find the deployed site [here](https://encheres-exclusives.herokuapp.com/). 

### Cloning

1. Start by creating a MongoDB account if you don't have one already. Create a cluster, and a database (here called encheres-privees).

2. My DB is organized as follow:

   ###### auctions

   ```
   _id: <ObjectId>
   category: <string>
   date_start: <date>
   date_end: <date>
   ```

   ###### lots

   ```
   _id: <ObjectId>
   category: <string>
   title: <string>
   brand_artist: <string>
   highest_bid: <int32>
   actual_bidder: <string>
   bid_time: <date>
   starting_price: <int32>
   estimated_price: <int32>
   reserve_price: <int32>
   image_url: <string>
   previous_bids_details: <array>
   	↳ { <object>
   		↳ [
   			previous_bidder: <string>
   			previous_bid: <int32>
   			previous_bid_time: <date>
   		]
   	}
   created_by: <string>
   creation_time: <date>
   ```

   ###### lots_sold

   ```
   _id: <ObjectId>
   category: <string>
   title: <string>
   brand_artist: <string>
   highest_bid: <int32>
   final_bidder: <string>
   final_bid_time: <date>
   estimated_price: <int32>
   image_url: <string>
   bids_history: <array>
   	↳ { <object>
   		↳ [
   			previous_bidder: <string>
   			previous_bid: <int32>
   			previous_bid_time: <date>
   		]
   	}
   sold_created_by: <string>
   creation_time: <date>
   ```

   ###### users

   ```
   _id: <ObjectId>
   email: <string>
   password: <string>
   title: <string>
   first_name: <string>
   last_name: <string>
   newsletter: <boolean>
   ```

   ###### newsletter

   ```
   _id: <ObjectId>
   email: <string>
   title: <string>
   first_name: <string>
   last_name: <string>
   ```

   

3. After you've copied the HTTPS or SSH link, located under the Code dropdown button on [Enchères Exclusives GitHub page](https://github.com/LuciusVH/encheres-exclusives).

4. Open your preferred IDE, create a virtual environment and activate it.

5. Run the command `git clone` + the link you've copied on step #1.

6. Create your environment file `env.py` and add the following:

   ```python
   import os
   from pymongo import MongoClient
   import certifi
   
   os.environ.setdefault("IP", "0.0.0.0")
   os.environ.setdefault("PORT", "5000")
   os.environ.setdefault("SECRET_KEY", "<YOUR SECRET KEY>")
   os.environ.setdefault("MONGO_URI", "<YOUR MONGODB URI>")
   os.environ.setdefault("MONGO_DBNAME", "<YOUR MONGODB DATABASE>")
   os.environ.setdefault("EMAIL_PSWD", "<YOUR EMAIL ACCOUNT PASSWORD>")
   
   s = MongoClient("<YOUR MONGODB URI>", tlsCAFile=certifi.where())
   ```

7. Create a `.gitignore` file and add it your `env.py`.

8. Install all the requirements: open the terminal and run `pip3 install -r requirements.txt`.

9. Switch `debug=False` to `debug=True` at the end of the `app.py` file.

10. You can now run the app with the command `python app.py`.

### Deployment

1. Create your own requirements.txt by typing the command `pip3 freeze --local > requirements.txt`

2. Create a Procfile by typing the command `echo web: python app.py > Procfile`. Make sure it's the exact same, with no extra whitespace or breakline.

3. Commit & push your change to GitHub.

4. Go to [Heroku](https://www.heroku.com/) & create an account if you don't already have one.

5. Create a new Python app, select your region.

6. On the Deploy tab, in the Connect to GitHub section: search for your repo and connect it. 

7. In the Settings tab, in the Config Vars section, enter:

   ```
   IP = 0.0.0.0
   PORT = 5000
   MONGO_DBNAME = <YOUR MONGODB DATABASE>
   MONGO_URI = <YOUR MONGODB URI>
   SECRET_KEY = <YOUR SECRET KEY>
   EMAIL_PSWD = <YOUR EMAIL ACCOUNT PASSWORD>
   ```

8. On the Deploy tab, in the Automatic Deploy section: select the `main` branch and click Enable Automatic Deploys.

## Credits

### Content

- All content has been written by myself.

### Media

- The hero pictures are both from Adobe Stock [[landscape](https://stock.adobe.com/images/panoramic-shot-of-auctioneer-talking-with-microphone-and-holding-picture-during-auction/325679020) & [portrait](https://stock.adobe.com/images/auctioneer-talking-with-microphone-and-holding-picture-during-auction/325679180)]. 
- For the lots' pictures, see the detailed media credits [here](https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/media-credits.md).

### Acknowledgements

- I want to thank the Code Institute tutors, which are always helpful and resourceful! As well as my mentor, for these productive sessions. 
- The wonderful Code Institute Slack community as well! You guys rock 💪

------

------

##### The final word...

These paintings, books... God if I had the money......... 🤑
