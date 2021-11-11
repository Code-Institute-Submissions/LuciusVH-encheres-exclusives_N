### Detailed Existing Features

- ##### Account features

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

  - **My Lots**

    A slider displays all the user own items, to be sold. Since they are the user's items, the usual "Place Bid" button is replaced by two buttons: *Edit* & *Delete*, for each item. The Edit button opens up the <u>Edit Item modal</u>, which is basically a copy of the <u>Add Item modal</u> (see below). 

  - **Propose a lot**

    This button opens up the <u>Add Item modal</u>, and allows the user to enter the details of their item to propose it to be auctioned. The user must specify *Title*, *Artist* or *Brand*, the *Estimated price* and a URL for the *Picture*. The *Starting Price* is automatically set to 10% of the *Estimated Price*. For the commercial version of this app, this lot would be submitted to approval before to be added to the database, and of course the *Estimated Price* and *Starting Price* would be proposed by the auction experts to the owner. The owner would also have to provide several pictures and the provenance documents in order for the item to be accepted. 

- ##### Auctions features

  - **Auctions navbar links**

    Auctions are held for a fortnite and the turnover is encoded within the [`auction_dispatch()`]() function **[LINK TO BE UPDATED]**. Through this function, the auctions dispatch themselves between two lists: `current_auctions` & `upcoming_auctions`. For each auction, the function will dispatch it in the correct list, based on the auction's `date_start` & `date_end` keys. 

    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/auction-dates-keys.png" alt="Picture of how the auctions are organised in the database"/>
    </p>

    When an auction is dispatched the `upcoming_auctions` list, the function also updates its date by incrementing them of 1 week * as many weeks auction categories there are. It's currently set to 70 days, since there are 7 days per week * 10 different auction categories. 

  - **Newest Auction slider**

    On the Home page, the newest auction is displayed. Although there are always two auctions running at the same time, this slider displays only the latest (the auction that started the most recently), using the `current_auctions` list, index `[0]`, since the auctions are sorted by `date_start` before to be dispatched. For a guest user, each "Place Bid" button will lead to the Login page. For a registered user, they open up the Bidding modal, allowing them to place their bid on their desired item. If an item has actually been proposed for auction by the same user, of course they cannot bid on their own item so instead they have access to two different buttons: *Edit* & *Delete*, which allow them to edit their item or delete it from the sale if they changed their mind. 

  - 