/**
 * Add event listener to handle form submission and validate password.
 * If the password and confirm password do not match, display an alert.
 **/

document.getElementById('signup-form').addEventListener('submit', function (event) {
    // Get the password and confirm password values from the input fields
    var password = document.getElementById('signupPassword').value;
    var confirmPassword = document.getElementById('confirm-password').value;

    // Check if the password and confirm password match
    if (password !== confirmPassword) {
        event.preventDefault(); // Prevent the form from being submitted

        // Create the alert element
        var alertElement = document.createElement('div');
        alertElement.className = 'alert alert-danger alert-dismissible fade show';
        alertElement.textContent = 'Passwords do not match';

        // Insert the alert element before the "signup-form" element
        var formContainer = document.querySelector('.form-container');
        formContainer.insertBefore(alertElement, document.getElementById('signup-form'));

        // Hide the alert after 3 seconds
        setTimeout(function () {
            alertElement.style.display = 'none';
        }, 3000);
    }
});
