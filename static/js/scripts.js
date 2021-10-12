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

  if (window.innerHeight >= window.innerWidth) {
    header.className = "hero-section bg-dark py-5 hero-img-portrait"
  } else {
    header.className = "hero-section bg-dark py-5 hero-img-landscape"
  }
}