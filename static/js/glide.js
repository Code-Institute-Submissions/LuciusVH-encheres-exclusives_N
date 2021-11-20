const config = {
  type: 'slider',
  startAt: 0,
  perView: 4,
  focusAt: 0,
  autoplay: 2000,
  hoverpause: true,
  gap: 15,
  breakpoints: {
    1200: {
      perView: 4
    },
    768: {
      perView: 3
    },
    576: {
      perView: 1
    }
  }
};

// Enable multiple sliders on the same page
// Code snippet found on https://github.com/glidejs/glide/issues/59#issuecomment-529124814 
const sliders = document.querySelectorAll('.glide');

Object.values(sliders).map(slideshow => {
  const slider = new Glide(slideshow, config);
  slider.mount();
});