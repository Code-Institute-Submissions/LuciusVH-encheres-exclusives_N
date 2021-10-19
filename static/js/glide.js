const config = {
  type: 'slider',
  startAt: 0,
  perView: 4,
  focusAt: 0,
  // autoplay: 2000,
  hoverpause: true,
  breakpoints: {
    1200: {
      perView: 3
    },
    768: {
      perView: 2
    },
    576: {
      perView: 1
    }
  }
};

new Glide('.glide', config).mount();