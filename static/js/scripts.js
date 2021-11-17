// Checkes if the user has scrolled down more than 20px and reduces the logo height in half (and so the navbar height)
window.onscroll = () => {
  scrollCheck();
}

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

// Adapts the hero img depending on the size of the header
window.onresize = changeBgImg;

function changeBgImg() {
  let header = document.querySelector('.hero-section');

  if (window.innerWidth <= 650) {
    header.className = "hero-section bg-dark py-5 hero-img-portrait";
  } else {
    header.className = "hero-section bg-dark py-5 hero-img-landscape";
  }
}

// Update copyright date
$(document).ready(function() {
  $('#copyright').text(new Date().getFullYear());
})


// Target the Delete link on profile page to toggle the delete profile confirmation toast
// or the delete button on profile page to toggle the delete item confirmation toast
const deleteToastSwitch = document.querySelectorAll('.delete-toast');
deleteToastSwitch.forEach((el) => {
  el.addEventListener('click', deleteToast);
})

function deleteToast() {
  let toastClicked = this.id;
  let lot_id = toastClicked.substr(12);

  const options = {
    autohide: false,
    animation: true
  }

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
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

// Custom error input when the user wants to bid a lower price than required
let userInput = document.querySelectorAll('input[name="user_bid"]');
userInput.forEach((el) => {
  el.addEventListener('change', bidInput);
})

function bidInput(event) {
  let input = event.target;
  let minValue = parseInt(input.getAttribute('min'));

  if (input.validity.rangeUnderflow) {
    input.setCustomValidity(`Your bid cannot be lower than ${minValue + 1}€`);
  } else {
    input.setCustomValidity('');
  }
}

// Calculate the Starting Price of a lot when the user fills up the Add lot form
let estimatedPriceInput = document.querySelector('#addlot-estimatedprice');
estimatedPriceInput.addEventListener('input', calculateStartingPrice)

function calculateStartingPrice() {
  let estimatedPrice = estimatedPriceInput.value;
  let startingPrice = estimatedPrice / 10;

  let startingPriceInput = document.querySelector('#addlot-startingprice');
  startingPriceInput.value = Math.round(startingPrice);
}

// Verify the URL input when the user fills up the Add/Edit lot form
let imageURLInput = document.querySelector('#addlot-imageurl');
imageURLInput.addEventListener('change', imageLoad);
let imageURLInputEditModal = document.querySelectorAll('.editlot-imageurl')
imageURLInputEditModal.forEach((el) => {
  el.addEventListener('change', imageLoadEditModal);
})

function imageLoad() {
  let submitBtn = document.querySelector('#addlot-submit-btn');
  let imagePreview = document.querySelector('#addlot-imagepreview');

  // Check if the URL ends with the correct image format
  if (imageURLInput.value.length != 0) {
    if (imageURLInput.value.endsWith('.jpg') || (imageURLInput.value.endsWith('.jpeg')) || (imageURLInput.value.endsWith('.png'))) {

      // Set the preview src & alt with the URL input & title/artist or brand
      imagePreview.setAttribute('src', imageURLInput.value);
      let imageTitle = document.querySelector('#addlot-title').value;
      let imageArtistBrand = document.querySelector('#addlot-artistbrand').value;
      imagePreview.setAttribute('alt', `${imageTitle} by ${imageArtistBrand}`);

      // If there's an error in the URL and no image loads, set the submit button to disabled, send an alert to the user to inform them
      imagePreview.onerror = () => {
        submitBtn.disabled = true;
        imagePreview.setAttribute('alt', 'Loading Error /!\\');
        alert("There's an error in your URL. Check it ;)");
      }

      // Otherwise, allow the user to submit their completed form
      imagePreview.onload = () => {
        if (imagePreview.src.endsWith('/static/img/no_pic.jpg')) {
          submitBtn.disabled = true;
        } else {
          submitBtn.disabled = false;
        }
      }
    } else {
      // Keep the default pic otherwise & inform the user they didn't set a correct image format
      imagePreview.setAttribute('src', '/static/img/no_pic.jpg');
      imagePreview.setAttribute('alt', "Question mark drawing, as there's no picture input yet");
      submitBtn.disabled = true;
      alert('Your image URL does not end by .jpg, .jpeg or .png');
    }
  } else {
    // Keep the default pic otherwise & inform the user they didn't set a correct image format
    imagePreview.setAttribute('src', '/static/img/no_pic.jpg');
    imagePreview.setAttribute('alt', "Question mark drawing, as there's no picture input yet");
    submitBtn.disabled = true;
    alert('You have to upload a picture of your item');
  }
}

function imageLoadEditModal() {
  let editModalOpened = this.id;
  let lot_id = editModalOpened.substr(17);
  let imageURLInputEditModalId = document.querySelector('#editlot-imageurl-' + lot_id);
  let imagePreviewEditModalId = document.querySelector('#editlot-imagepreview-' + lot_id);
  let submitBtnEditModalId = document.querySelector('#editlot-submit-btn-' + lot_id);

  // Check if the URL ends with the correct image format
  if (imageURLInputEditModalId != 0) {
    if (imageURLInputEditModalId.value.endsWith('.jpg') || (imageURLInputEditModalId.value.endsWith('.jpeg')) || (imageURLInputEditModalId.value.endsWith('.png'))) {
      // Set the preview src & alt with the URL input & title/artist or brand
      imagePreviewEditModalId.setAttribute('src', imageURLInputEditModalId.value);
      let imageTitleEditModalId = document.querySelector('#editlot-title-' + lot_id).value;
      let imageArtistBrandEditModalId = document.querySelector('#editlot-artistbrand-' + lot_id).value;
      imagePreviewEditModalId.setAttribute('alt', `${imageTitleEditModalId} by ${imageArtistBrandEditModalId}`);

      // If there's an error in the URL and no image loads, set the submit button to disabled, send an alert to the user to inform them
      imagePreviewEditModalId.onerror = () => {
        submitBtnEditModalId.disabled = true;
        imagePreviewEditModalId.setAttribute('alt', 'Loading Error /!\\');
        alert("There's an error in your URL. Check it ;)");
      }

      // Otherwise, allow the user to submit their completed form
      imagePreviewEditModalId.onload = () => {
        if (imagePreviewEditModalId.src.endsWith('/static/img/no_pic.jpg')) {
          submitBtnEditModalId.disabled = true;
        } else {
          submitBtnEditModalId.disabled = false;
        }
      }
    } else {
      // Keep the default pic otherwise & inform the user they didn't set a correct image format
      imagePreviewEditModalId.setAttribute('src', '/static/img/no_pic.jpg');
      imagePreviewEditModalId.setAttribute('alt', "Question mark drawing, as there's no picture input yet");
      submitBtnEditModalId.disabled = true;
      alert('Your image URL does not end by .jpg, .jpeg or .png');
    }
  } else {
    // Keep the default pic otherwise & inform the user they didn't set a correct image format
    imagePreviewEditModalId.setAttribute('src', '/static/img/no_pic.jpg');
    imagePreviewEditModalId.setAttribute('alt', "Question mark drawing, as there's no picture input yet");
    submitBtnEditModalId.disabled = true;
    alert('You have to upload a picture of your lot');
  }
}