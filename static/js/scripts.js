window.onscroll = () => {
  scrollCheck()
};

function scrollCheck() {
  let logo = document.querySelector('.logo');

  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    logo.style.height = '30px';
  } else {
    logo.style.height = '60px';
  }
}