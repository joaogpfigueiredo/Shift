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