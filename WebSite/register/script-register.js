var password = document.getElementById("password");
var confirm_password = document.getElementById("confirm_password");

function validatePassword(){
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("The Passwords Don't Match!");
  } else {
    confirm_password.setCustomValidity('');
  }
}