var password = document.getElementById("password");
var confirm_password = document.getElementById("confirm_password");

function validatePassword(){
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("The Passwords Don't Match!");
  } else {
    confirm_password.setCustomValidity('');
  }
}

function menuClick() {
  var list = document.querySelector('menu.list');

  list.classList.toggle('active');
}

document.addEventListener("DOMContentLoaded", function() {
  
  var urlParams = new URLSearchParams(window.location.search);
  var errorMessage = urlParams.get('error');
  
  
  if (errorMessage) {
      alert(errorMessage);
      
      window.history.replaceState({}, document.title, window.location.pathname);
  }
});