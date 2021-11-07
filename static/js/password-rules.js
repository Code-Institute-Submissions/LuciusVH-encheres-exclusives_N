// Show the password instructions when the user selects the password field when registering or updating their profile
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