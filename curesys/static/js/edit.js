document.addEventListener("DOMContentLoaded", function() {
    // Retrieve user details from local storage
    var firstName1 = localStorage.getItem('firstName');
    var lastName1 = localStorage.getItem('lastName');
    var email1 = localStorage.getItem('email');
    var phone1 = localStorage.getItem('phone');
    var mobile1 = localStorage.getItem('mobile');
    var address1 = localStorage.getItem('address');
    var dob1 = localStorage.getItem('dob');

    // Display user details in the HTML
    document.getElementById('firstNameValue').innerHTML = firstName1;
    document.getElementById('lastNameValue').innerHTML = lastName1;
    document.getElementById('emailValue').innerHTML = email1;
    document.getElementById('phoneValue').innerHTML = phone1;
    document.getElementById('mobileValue').innerHTML = mobile1;
    document.getElementById('addressValue').innerHTML = address1;
    document.getElementById('dobValue').innerHTML = dob1;
});
