// Checkes if the user has scrolled down more than 20px and reduces the logo height in half (and so the navbar height)
window.onscroll = () => {
  scrollCheck();
};

function scrollCheck() {
  let logo = document.querySelector('.logo');
  let nav = document.querySelector('nav');

  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    logo.style.height = '30px';
    nav.classList.add('navbar-shadow');
  } else {
    logo.style.height = '60px';
    nav.classList.remove('navbar-shadow');
  }
}

// Update copyright date
$(document).ready(function() {
  $('#copyright').text(new Date().getFullYear());
});

// Target the Delete link on profile page to toggle the delete profile confirmation toast
// or the delete button on profile page to toggle the delete item confirmation toast
const deleteToastSwitch = document.querySelectorAll('.delete-toast');
deleteToastSwitch.forEach((el) => {
  el.addEventListener('click', deleteToast);
});

function deleteToast() {
  let toastClicked = this.id;
  let lot_id = toastClicked.substr(11);

  const options = {
    autohide: false,
    animation: true
  };

  if (toastClicked == "delete-profile") {
    const deleteProfileToast = document.querySelector('#delete-profile-confirmation');
    const deleteProfileToastBuild = new bootstrap.Toast(deleteProfileToast, options);
    deleteProfileToastBuild.show();
  } else if (toastClicked == `delete-lot-${lot_id}`) {
    const deletelotToast = document.querySelector(`#delete-lot-confirmation-${lot_id}`);
    const deletelotToastBuild = new bootstrap.Toast(deletelotToast, options);
    deletelotToastBuild.show();
  }
}

// Enable Bootstrap tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Custom error input when the user wants to bid a lower price than required
let userInput = document.querySelectorAll('input[name="user_bid"]');
userInput.forEach((el) => {
  el.addEventListener('change', bidInput);
});

function bidInput(event) {
  let input = event.target;
  let minValue = parseInt(input.getAttribute('min'));

  if (input.validity.rangeUnderflow) {
    input.setCustomValidity(`Your bid cannot be lower than ${minValue + 1}€`);
  } else {
    input.setCustomValidity('');
  }
}

// Calculate the Starting Price & Reserve Price of a lot when the user fills up the Add lot form
let estimatedPriceInput = document.querySelector('#addlot-estimatedprice');
estimatedPriceInput.addEventListener('input', calculatePrices);

function calculatePrices() {
  let estimatedPrice = estimatedPriceInput.value;
  let startingPrice = estimatedPrice / 10;
  let reservePrice = estimatedPrice / 2;

  let startingPriceInput = document.querySelector('#addlot-startingprice');
  startingPriceInput.value = Math.round(startingPrice);
  let reservePriceInput = document.querySelector('#addlot-reserveprice');
  reservePriceInput.value = Math.round(reservePrice);
}