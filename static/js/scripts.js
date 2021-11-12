// Checkes if the user has scrolled down more than 20px and reduces the logo height in half (and so the navbar height)
window.onscroll = () => {
  scrollCheck()
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

// Adapts the hero img depending on the size of the header
window.onresize = changeBgImg;

function changeBgImg() {
  let header = document.querySelector('.hero-section');

  if (window.innerWidth <= 650) {
    header.className = "hero-section bg-dark py-5 hero-img-portrait"
  } else {
    header.className = "hero-section bg-dark py-5 hero-img-landscape"
  }
}

// Update copyright date
$(document).ready(function() {
  $('#copyright').text(new Date().getFullYear());
})


// Target the Delete link on profile page to toggle the delete profile confirmation toast
const deleteToastSwitch = document.querySelectorAll('.delete-toast');
deleteToastSwitch.forEach((el) => {
  el.addEventListener('click', deleteToast);
});

function deleteToast() {
  let toastClicked = this.id
  let item_id = toastClicked.substr(12)
  console.log(item_id)

  const options = {
    autohide: false,
    animation: true
  }

  if (toastClicked == "delete-profile") {
    const deleteProfileToast = document.querySelector('#delete-profile-confirmation')
    const deleteProfileToastBuild = new bootstrap.Toast(deleteProfileToast, options)
    deleteProfileToastBuild.show()
  } else if (toastClicked == `delete-item-${item_id}`) {
    const deleteItemToast = document.querySelector(`#delete-item-confirmation-${item_id}`)
    const deleteItemToastBuild = new bootstrap.Toast(deleteItemToast, options)
    deleteItemToastBuild.show()
  }
}

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