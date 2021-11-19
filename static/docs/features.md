### Detailed Existing Features

- ##### App features

  - **Newsletter subscription**

    The app offers the possibility to subscribe to the company's newsletter, without having to get an account. It checks in the newsletter collection if the email isn't already present, and warn the user if that's the case through a Flash message. 

  - **Flash messages**

    Each time the user does something related to the database (any of the CRUD operation), a Flash message appears on the bottom of the screen, using [Bootstrap Toast](https://getbootstrap.com/docs/5.0/components/toasts/) component. Depending on the message content, an icon goes with it:

    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/flash-messages.png" alt="Different Flash messages."/>
    </p>

  - **Contact function**

    The contact form is linked to the email address ms3.encheres.privees@gmail.com, through the [yagmail](https://github.com/kootenpv/yagmail) extension. When a user sends an email through the app contact form, the address ms3.encheres.privees@gmail.com sends an email to itself, detailing the sender's details & message:

    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/test-email.png" alt="Email received after using the app contact form."/>
    </p>

    The user gets a confirmation with Flash message, whether it went through or not. If something goes wrong, the Flash messages invites them to contact ms3.encheres.privees@gmail.com directly:

    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/contact-flash-message.png" alt="Flash confirmation or error message."/>
    </p>

- **Account features**

  - **Register / Log In / Log Out / Edit / Delete functions**

    The user must register and become a member in order to place a bid and sold their lot(s). They can log in to their account, and log out. They can edit their data and delete it (delete the account). From the register form (and updating form) they can opt in or out for the newsletter subscription.

  - **Security**

    A user cannot access, edit or delete another user's profile. These functions are linked to the user logged-in via `session`.

  - **Passport instructions**

    The passport instructions (6 to 20 characters long, must contain one digit, one lower and one uppercase letter) are displayed in a popup, only when the passport field is focused, on the registration form (and <u>Edit Profile page</u>). 

    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/password-instructions.gif" alt="GIF showing off the passport instructions popup."/>
    </p>

  - **Profile data update**

    When updating their profile data, all data is prepopulated except the password. If they leave the field blank, the password remain unchanged, if they fill up the password field (with a correct input, matching the instructions) then it is updated. This feature is to avoid the user having to retype their password anytime they want to change something else.

  - **Profile deletion**

    A user can delete their profile, using the *Delete* link on the <u>Profile page</u>. This will prompt up a confirmation alert, informing them that they are about to delete their profile, which includes their potential bid(s) & lot(s). If they choose to proceed, before to actually delete their entry from the `users` collection, the function will indeed suppress their items from the `lots` collection, and run through the same collection to proceed eventual changes in the bids order. 

    If the user holds the current highest bid, this bid is then deleted and the function pulls up the previous bidder's details instead from the `previous_bidds_details` array.

  - **My Bids**

    A slider displays all the lots on which the user has bidden, while they has been outbidden or not. Way to keep track on your bids! 

  - **My Lots**

    A slider displays all the user own lots, to be sold. Since they are the user's lots, the usual *Place Bid* button is replaced by two buttons: *Edit* & *Delete*, for each lot. The *Edit* button opens up the <u>Edit lot modal</u>, which is basically a copy of the <u>Add lot modal</u> (see below). The *Delete* button opens a "Toast", asking for the user's confirmation before to delete the lot. These buttons are disabled if the auction's category to which the lot belongs has started already. 

  - **Auction's over**
  
    This third section appears on the <u>Profile page</u>, when an auction is over and the user has either way won at least one auction, or they had lots in this auction which have been sold. The usual *Place Bid*, *Edit* or *Delete* buttons on the lot card are replaced by a *You won!* / *Sold!* button, depending on the situation. This button links to the contact page, inviting the user to get in touch with *Enchères Privées* to manage the payment or the reception of their money. 

- ##### Auctions features

  - **Auctions navbar links**

    Auctions are held for a fortnite and the turnover is encoded within the [`auction_dispatch()`]() function **[LINK TO BE UPDATED]**. Through this function, the auctions dispatch themselves between two lists: `current_auctions` & `upcoming_auctions`. For each auction, the function will dispatch it in the correct list, based on the auction's `date_start` & `date_end` keys. 

    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/auction-dates-keys.png" alt="Picture of how the auctions are organised in the database."/>
    </p> 
    
    When an auction is dispatched the `upcoming_auctions` list, the function also updates its date by incrementing them of 1 week * as many weeks auction categories there are. It's currently set to 70 days, since there are 7 days per week * 10 different auction categories.

  - **Newest Auction slider**

    On the <u>Home page</u>, the newest auction is displayed. Although there are always two auctions running at the same time, this slider displays only the latest (the auction that started the most recently), using the `current_auctions` list, index `[0]`, since the auctions are sorted by `date_start` before to be dispatched. 

    For a guest user, each "Place Bid" button will lead to the <u>Login page</u>. For a registered user, they open up the <u>Bidding modal</u>, allowing them to place their bid on their desired lot. If an lot has actually been proposed for auction by the same user, of course they cannot bid on their own lot so instead they have access to two different buttons: *Edit* & *Delete*, which allow them to edit their lot or delete it from the sale if they changed their mind. 

  - **Place Bid button & Bidding modal**

    On each lot's card, the *Place Bid* button links to the <u>Login page</u> if the user is not already logged-in, else it opens up the <u>Bidding modal</u>. Also, this button is shown to logged-in user who are not the owner of the lot. You cannot bid on your own lot, in all logic.

    The <u>Bidding modal</u> display basic information on the selected lot: *Title*, *Artist* or *Brand*, *Estimated Price*, and either *Starting Price* if no bid has been proposed yet, or the *Actual Bid* otherwise. Finally, the user can insert their bid. The form is subject to a minimal amount verification: the user cannot bid less than the Actual Bid/Starting Price + 1€, as shown with a customized alert message:

    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/min-bid-alert.png" alt="Alert message informing the user their bid does not reach the minimum amount required."/>
    </p>

  - **Propose a lot**

    This button, accessible from the <u>Profile page</u>, opens up the <u>Add lot modal</u>, and allows the user to enter the details of their lot to propose it to be auctioned. The user must specify *Title*, *Artist* or *Brand*, the *Estimated price* and a URL for the *Picture*. The *Starting Price* is automatically set to 10% of the *Estimated Price*. For the commercial version of this app, this lot would be submitted to approval before to be added to the database, and of course the *Estimated Price* and *Starting Price* would be proposed by the auction experts to the owner. The owner would also have to provide several pictures and the provenance documents in order for the lot to be accepted. 

    The *Image Preview* allows the user to visualize their chosen image, mostly to verify if they did not make a mistake in their URL. 

    The *Submit button* is disabled until the user has provided a correct image (JPEG or PNG + URL being valid).
    
  - **Edit or Delete a lot**

    A user can obviously only edit/delete their own lot. The *Edit* button opens up the <u>Edit lot modal</u>, which is basically a copy of the <u>Add lot modal</u> (see above). The *Delete* button opens a "Toast", asking for the user's confirmation before to delete the lot. These buttons are only available as the auction's category they belong to has not started yet. Otherwise, they are disabled:

    <p align="center">
      <img src="https://github.com/LuciusVH/encheres-exclusives/blob/main/static/docs/readme-img/disabled-action-buttons.png" alt="Disabled Edit/Delete buttons on the user's lots."/>
    </p>