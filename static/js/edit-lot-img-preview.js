// Verify the URL input when the user fills up the Edit lot form
var imageURLInputEditModal = document.querySelectorAll('.editlot-imageurl')
imageURLInputEditModal.forEach((el) => {
  el.addEventListener('change', imageLoadEditModal);
})

function imageLoadEditModal() {
  var editModalOpened = this.id;
  var lot_id = editModalOpened.substr(17);
  var imageURLInputEditModalId = document.querySelector('#editlot-imageurl-' + lot_id);
  var imagePreviewEditModalId = document.querySelector('#editlot-imagepreview-' + lot_id);
  var submitBtnEditModalId = document.querySelector('#editlot-submit-btn-' + lot_id);

  // Check if the URL ends with the correct image format
  if (imageURLInputEditModalId != 0) {
    if (imageURLInputEditModalId.value.endsWith('.jpg') || (imageURLInputEditModalId.value.endsWith('.jpeg')) || (imageURLInputEditModalId.value.endsWith('.png'))) {
      // Set the preview src & alt with the URL input & title/artist or brand
      imagePreviewEditModalId.setAttribute('src', imageURLInputEditModalId.value);
      var imageTitleEditModalId = document.querySelector('#editlot-title-' + lot_id).value;
      var imageArtistBrandEditModalId = document.querySelector('#editlot-artistbrand-' + lot_id).value;
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