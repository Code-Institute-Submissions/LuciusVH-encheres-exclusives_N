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
   3. [Bugs](https://github.com/LuciusVH/encheres-exclusives#bugs)
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

The world of auctions known for selling famous artworks and extremely expensive items, is sometimes perceived as too closed or secret. It is a common misperception, turns out more than 90% of the auctions in the world are completely public and accessible to anyone who dares to cross the doorstep. This misconception is due to the fact that we only hear about the exceptional sales, proposing extraordinary lots, often reserved to already well known customers of the auction house hosting the event. *Enchères Exclusives* is a gateway to this realm, with the mission to make it more accessible, even from the comfort of your living room.

### 	Structure & Design

Designed as a multipage website, built with Flask, it allows the user to browse the different collections, create an account to bid on some items of their liking, and sold some of their own. *Enchères Exclusives* also gives some precious information about the auction business, in order to familiarize the user and sort of demystify this world. 

I wanted the general design to stay clean and sleek, to allow the user to focus on the items. The color panel is really neutral with Ghost White (#F8F8FF) and Gray80 (#CCCCCC) as background color when an element needs a bit more attention (like for a title banner). The global text color is also a gray, Gray20 (#333333). To highlight some elements, I used different shades of *Enchères Exclusives*'s indigo (#23448D). All contrast ratios were tested using [WebAIM.org contrast checker](https://webaim.org/resources/contrastchecker/). 

The <u>Home page</u> displays a hero image, the image being different depending on the viewport's width, to ensure a nice rendering on any screen. 

Below this, the latest auction is exposed, showing off the items in a carousel, each item presented in a card. The number of cards depends on the width available: from 1 to 4. 

Next comes a section inviting the user to subscribe to the company's newsletter. This section is shown only if the user hasn't subscribed already.

Finally, a footer inviting the user to follow *Enchères Exclusives* on different social medias: Twitter, Facebook, Instagram, YouTube & Weibo. A discreet copyright mention is positioned under it, being aligned with the "Follow us" on desktop, or centered from a smaller screen. 

The navigation bar is pretty basic: the company's logo on the left, being a link to the homepage. Then 2 sections of links: on the left the company's related links with "Auctions", "About" & "Contact" ; On the right side, "Sign In / Sign Up" and a "Search" bar. All these links collapse on tablet & phone screen, under a hamburger icon, right-positioned. It opens up a dropdown menu, displaying all the same links. Finally, from a computer, the logo gets reduced by half once the user starts scrolling down the page (while it's automatically set to 30px height on phone & tablet screens), giving more space to the content, and a shadow appears under the navbar to create a separation between the navbar and the rest of the website, both having the same background color. 

Auction link

About link

<u>Contact modal</u>

The <u>Register page</u> simply display a form with 4 input fields (email, password, first name & last name), a dropdown to select your appropriate title, a checkbox to receive the newsletter and a "Sign Up" button. Under that, a "Log In" link if the user misclicked and already is a member. Once validated, the user is redirected to the Profile page.

The <u>Login page</u> is also pretty simple: a form with 2 input fields (email & password), a "Log In" button. Under that, a "Sign Up" button as an invitation, if the user doesn't have an account already. Once validated, the user is redirected to the Profile page.

The <u>Profile page</u> display a personalized welcoming message followed by the user's data: full name (title, first name & last name), the email and "* * * * * *" as password. Below these are two links, allowing the user to *Edit* or *Delete* their profile. The links are discreet, as I did not want them to be so obviously visible as buttons or icons can be. Although it's a nice feature, I did not wanted it to take too much focus. 

Clicking on *Edit* leads the user to the <u>Edit Profile page</u>, of course, which is a copy of the Register page. The form is already populated with the user data registered in the database. As of now, I have an issue to prepopulate the title dropdown with the correct content (more on this in the [bugs](https://github.com/LuciusVH/encheres-exclusives#bugs) section).

The *Delete* link opens up a Bootstrap "toast", playing the alert role (it is set up by aria attributes, for screen-readers): it asks the user for confirmation that they really want to delete their account, informing them that all data will be deleted with no possibility to cancel this action. 

### User stories

- As a buyer, I want to find new items my collections. 
- As a user, I want to find information about the actual & upcoming sales. 
- As a seller & member, I want to resell some of my items. 
- As a buyer & member, I want to see my bids.
- As a user, I want to find information about the company's offices.
- As a buyer/seller, I want to find information about the whole process & how this works.
- As a seller & member, I want to be able to add my item to be sold, edit or delete them.
- As a member, I want to be able to edit or delete my profile.
- As a new user, I want to be able to create an account.
- As a user, I want to subscribe to the newsletter.
- As a user, I want to learn more about the auction world.

### Bugs

- **Edit page form "title" dropdown prepopulation**

  The form is supposed to be populated with all user's data. It works fine with other fields, but I can't seem to get this dropdown to display the correct title. The "*selected*" attribute is set to "Ms", as it is the first option in the list.

  <p align="center">
    <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/dropdown-prepopulated.png" alt="Bug with dropdown list selected option"/>
  </p>

  <p align="center">
    <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/dropdown-prepopulated2.png" alt="Not matching the database data"/>
  </p>

  <u>Solution:</u> N/A

- 


## Features

### Existing Features

- **Register / Log In / Log Out / Edit / Delete functions**

  The user must register and become a member in order to place a bid and sold their item(s). They can log in their account, and log out. They can edit their data and delete it (delete the account). From the register form (and updating form) they can opt in or out for the newsletter.

- **Passport instructions**

  The passport instructions (6 to 20 characters long, must contain one digit, one lower and one uppercase letter) are displayed in a popup, only when the passport field is focused, on the registration form. 

  <p align="center">
    <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/password-instructions.gif" alt="gif showing off the passport instructions popup"/>
  </p>

- **Profile data update**

  When updating their profile data, all data is prepopulated except the password. If they leave the field blank, the password remain unchanged, if they fill up the password field (with a correct input, matching the instructions) then it is updated. This feature is to avoid the user having to retype their password anytime they want to change something else.
  
- **Newsletter subscription**

  The app offers the possibility to subscribe to the company's newsletter, without having to get an account. It checks in the newsletter collection if the email isn't already present, and warn the user if that's the case through a Flash message. 

### Features Left to Implement

- Password lost function



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
  - **Typora** was used to write this README file.
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



#### Tested user stories:



## Deployment & cloning

You can find the deployed site [here](https://encheres-exclusives.herokuapp.com/). 

### Deployment

### Cloning



## Credits

### Content

- X

### Media

- The hero pictures are both from Adobe Stock [[landscape](https://stock.adobe.com/images/panoramic-shot-of-auctioneer-talking-with-microphone-and-holding-picture-during-auction/325679020) & [portrait](https://stock.adobe.com/images/auctioneer-talking-with-microphone-and-holding-picture-during-auction/325679180)]. 

### Acknowledgements

- X 

