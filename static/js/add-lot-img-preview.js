// Verify the URL input when the user fills up the Add lot form
let imageURLInput = document.querySelector('#addlot-imageurl');
imageURLInput.addEventListener('change', imageLoad);

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