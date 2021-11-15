### Detailed Existing Features

- ##### Account features

  - **Register / Log In / Log Out / Edit / Delete functions**

    The user must register and become a member in order to place a bid and sold their item(s). They can log in to their account, and log out. They can edit their data and delete it (delete the account). From the register form (and updating form) they can opt in or out for the newsletter subscription.

  - **Security**

    A user cannot access, edit or delete another user's profile, even if they may have the other user's ID. I have chosen to use MongoDB automatically set ID instead of username to increase security. It's obviously much harder to find than a simple username. Furthermore, each accessing/editing/deleting function verifies first that the user is logged-in (otherwise returning them to the <u>Login page</u>) and then that the logged-in user matches with the profile's ID they are trying to perform an action on.

  - **Passport instructions**

    The passport instructions (6 to 20 characters long, must contain one digit, one lower and one uppercase letter) are displayed in a popup, only when the passport field is focused, on the registration form (and <u>Edit Profile page</u>). 

    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/password-instructions.gif" alt="GIF showing off the passport instructions popup."/>
    </p>

  - **Profile data update**

    When updating their profile data, all data is prepopulated except the password. If they leave the field blank, the password remain unchanged, if they fill up the password field (with a correct input, matching the instructions) then it is updated. This feature is to avoid the user having to retype their password anytime they want to change something else.

  - **Newsletter subscription**

    The app offers the possibility to subscribe to the company's newsletter, without having to get an account. It checks in the newsletter collection if the email isn't already present, and warn the user if that's the case through a Flash message. 

  - **Flash messages**

    Each time the user does something related to the database (any of the CRUD operation), a Flash message appears on the bottom of the screen, using [Bootstrap Toast](https://getbootstrap.com/docs/5.0/components/toasts/) component. Depending on the message content, an icon goes with it:

    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/flash-messages.png" alt="Different Flash messages."/>
    </p>

  - **My Lots**

    A slider displays all the user own items, to be sold. Since they are the user's items, the usual *Place Bid* button is replaced by two buttons: *Edit* & *Delete*, for each item. The *Edit* button opens up the <u>Edit Item modal</u>, which is basically a copy of the <u>Add Item modal</u> (see below). The *Delete* button opens a "Toast", asking for the user's confirmation before to delete the item.

- ##### Auctions features

  - **Auctions navbar links**

    Auctions are held for a fortnite and the turnover is encoded within the [`auction_dispatch()`]() function **[LINK TO BE UPDATED]**. Through this function, the auctions dispatch themselves between two lists: `current_auctions` & `upcoming_auctions`. For each auction, the function will dispatch it in the correct list, based on the auction's `date_start` & `date_end` keys. 

    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/auction-dates-keys.png" alt="Picture of how the auctions are organised in the database."/>
    </p>

  
    When an auction is dispatched the `upcoming_auctions` list, the function also updates its date by incrementing them of 1 week * as many weeks auction categories there are. It's currently set to 70 days, since there are 7 days per week * 10 different auction categories. 
  
  - **Newest Auction slider**
  
    On the <u>Home page</u>, the newest auction is displayed. Although there are always two auctions running at the same time, this slider displays only the latest (the auction that started the most recently), using the `current_auctions` list, index `[0]`, since the auctions are sorted by `date_start` before to be dispatched. 
  
    For a guest user, each "Place Bid" button will lead to the <u>Login page</u>. For a registered user, they open up the <u>Bidding modal</u>, allowing them to place their bid on their desired item. If an item has actually been proposed for auction by the same user, of course they cannot bid on their own item so instead they have access to two different buttons: *Edit* & *Delete*, which allow them to edit their item or delete it from the sale if they changed their mind. 
  
  - **Place Bid button & Bidding modal**
  
    On each item's card, the *Place Bid* button links to the <u>Login page</u> if the user is not already logged-in, else it opens up the <u>Bidding modal</u>. Also, this button is shown to logged-in user who are not the owner of the item. You cannot bid on your own item, in all logic.
  
    The <u>Bidding modal</u> display basic information on the selected item: *Title*, *Artist* or *Brand*, *Estimated Price*, and either *Starting Price* if no bid has been proposed yet, or the *Actual Bid* otherwise. Finally, the user can insert their bid. The form is subject to a minimal amount verification: the user cannot bid less than the Actual Bid/Starting Price + 1€, as shown with a customized alert message:
  
    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/min-bid-alert.png" alt="Alert message informing the user their bid does not reach the minimum amount required."/>
    </p>
  
  - **Propose a lot**
  
    This button, accessible from the <u>Profile page</u>, opens up the <u>Add Item modal</u>, and allows the user to enter the details of their item to propose it to be auctioned. The user must specify *Title*, *Artist* or *Brand*, the *Estimated price* and a URL for the *Picture*. The *Starting Price* is automatically set to 10% of the *Estimated Price*. For the commercial version of this app, this lot would be submitted to approval before to be added to the database, and of course the *Estimated Price* and *Starting Price* would be proposed by the auction experts to the owner. The owner would also have to provide several pictures and the provenance documents in order for the item to be accepted. 
  
    The *Image Preview* allows the user to visualize their chosen image, mostly to verify if they did not make a mistake in their URL. 
  
    The *Submit button* is disabled until the user has provided a correct image (JPEG or PNG + URL being valid).