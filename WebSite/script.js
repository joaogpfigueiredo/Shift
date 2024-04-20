function menuClick() {
    var list = document.querySelector('menu.list');

    list.classList.toggle('active');
}

function getintouchSent() {
    var name = document.getElementById('name');
    var email = document.getElementById('email');
    var message = document.getElementById('message');
    var accept = document.getElementById( 'accept');
    
    if  (name.value == '' || email.value == ''  || message.value.length < 50 || !accept.checked) {
        alert("Please fill out all fields!");
        return false;
    } else {
        alert("We'll be in touch with you soon!");
    }
}