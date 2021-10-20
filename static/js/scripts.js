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

document.querySelector('#copyright').text(new Date().getFullYear())

// Show the password instructions when the user selects the password field when registering
const passportField = document.querySelector('.password-register');
const passportInstructions = document.querySelector('.password-instructions');

passportField.addEventListener('focus', showInstructions);
passportField.addEventListener('blur', hideInstructions);

function showInstructions() {
  passportInstructions.style.display = 'block';
}

function hideInstructions() {
  passportInstructions.style.display = 'none';
}


// Target the Delete link on profile page to toggle the delete profile confirmation toast
function deleteToast() {
  const options = {
    autohide: false,
    animation: true
  }

  const deleteProfileToast = document.querySelector('#delete-profile-confirmation')
  const toast = new bootstrap.Toast(deleteProfileToast, options)
  toast.show()
}