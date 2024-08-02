const navbarMenu = document.querySelector(".navbar .links");
const hamburgerBtn = document.querySelector(".hamburger-btn");
const hideMenuBtn = navbarMenu.querySelector(".close-btn");
const showPopupBtn = document.querySelector(".login-btn");
const formPopup = document.querySelector(".form-popup");
const hidePopupBtn = formPopup.querySelector(".close-btn");
const signupLoginLink = formPopup.querySelectorAll(".bottom-link a");


const loginbutton = document.querySelector('.loginbtn');
const signupbutton = document.querySelector('.signupbtn');
const emailInput = document.querySelector('.email-field');
const passwordInput = document.querySelector('.password-field');


// Show mobile menu
hamburgerBtn.addEventListener("click", () => {
    navbarMenu.classList.toggle("show-menu");
});
// Hide mobile menu
hideMenuBtn.addEventListener("click", () =>  hamburgerBtn.click());
// Show login popup
showPopupBtn.addEventListener("click", () => {
    document.body.classList.toggle("show-popup");
});
// Hide login popup
hidePopupBtn.addEventListener("click", () => showPopupBtn.click());
// Show or hide signup form
signupLoginLink.forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        formPopup.classList[link.id === 'signup-link' ? 'add' : 'remove']("show-signup");
    });
});

//  for checking maild,password
document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.querySelector('.form-popup .login form');
    const signupForm = document.querySelector('.form-popup .signup form');

    // Function to validate email format
    function isValidEmail(email) {
        // Regular expression for email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Function to check password requirements
    function isStrongPassword(password) {
        // Regular expressions for password requirements
        const minLength = 8;
        const hasNumber = /\d/;
        const hasUpperCase = /[A-Z]/;
        const hasLowerCase = /[a-z]/;

        return (
            password.length >= minLength &&
            hasNumber.test(password) &&
            hasUpperCase.test(password) &&
            hasLowerCase.test(password)
        );
    }

    // Event listener for login form submission
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const emailInput = loginForm.querySelector('input[type="text"]');
        const passwordInput = loginForm.querySelector('input[type="password"]');

        // Validate email
        if (!isValidEmail(emailInput.value)) {
            alert('Please enter a valid email address.');
            return;
        }

        // Validate password
        if (!isStrongPassword(passwordInput.value)) {
            alert('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.');
            return;
        }

        // Submit form if everything is valid (you can replace this with your own logic)
        loginForm.submit();
        // redirectToChatbotPage();

    });

    // Function to redirect to the chatbot page
    function redirectToChatbotPage() {
        window.location.href = '/chatbot'; // Redirect to the chatbot page URL
    }



    // Event listener for signup form submission
    signupForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const emailInput = signupForm.querySelector('input[type="text"]');
        const passwordInput = signupForm.querySelector('input[type="password"]');
        const policyCheckbox = signupForm.querySelector('#policy');

        // Validate email
        if (!isValidEmail(emailInput.value)) {
            alert('Please enter a valid email address.');
            return;
        }

        // Validate password
        if (!isStrongPassword(passwordInput.value)) {
            alert('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.');
            return;
        }

        // Validate if policy checkbox is checked
        if (!policyCheckbox.checked) {
            alert('Please agree to the Terms & Conditions.');
            return;
        }

        // Submit form if everything is valid (you can replace this with your own logic)
        signupForm.submit();
    });
});


// for password visibility
document.addEventListener('DOMContentLoaded', function () {
    const togglePasswordIcons = document.querySelectorAll('.toggle-password');
    
    togglePasswordIcons.forEach(function(icon) {
        icon.addEventListener('click', function() {
            // Find the closest parent form element
            const form = icon.closest('form');
            
            // Find the password field within the same form
            const passwordField = form.querySelector('.password-field');
            
            // Toggle the visibility of the password field
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            
            // Update the icon text
            icon.textContent = type === 'password' ? 'visibility_off' : 'visibility';
        });
    });
});

// calculator popup
const showCalPop = document.querySelector(".cutcal");

const calculatorPopup = document.querySelector(".calculator-popup");

showCalPop.addEventListener("click", () => {
    document.body.classList.toggle("show-calpopup");
});

const hidecalPop = document.querySelector(".calculator-popup .close-btn");
hidecalPop.addEventListener("click", () => showCalPop.click());

// cutoff calculator result
// Select form and result element
const marksForm = document.getElementById('marks-form');
const resultElement = document.getElementById('result');

// Add event listener to form submit
marksForm.addEventListener('submit', function(event) {
    // Prevent default form submission
    event.preventDefault();

    // Get marks entered by the user
    const physicsMark = parseFloat(document.getElementById('physics-mark').value);
    const chemistryMark = parseFloat(document.getElementById('chemistry-mark').value);
    const mathsMark = parseFloat(document.getElementById('maths-mark').value);

    // Calculate cutoff score
    if (isValidMark(physicsMark) && isValidMark(chemistryMark) && isValidMark(mathsMark)) {
        // Calculate cutoff score
        const cutoffScore = (physicsMark / 2) + (chemistryMark / 2) + mathsMark;

        // Display result on the screen
        resultElement.textContent = `Cutoff Score: ${cutoffScore.toFixed(2)}`;
    } else {
        // Display error message if marks are not within the range
        resultElement.textContent = "Please enter valid marks between 0 and 100.";
    }
});

// Function to validate marks
function isValidMark(mark) {
    return !isNaN(mark) && mark >= 0 && mark <= 100;
}


 // clearing input fields
const closeBtn = document.querySelector(".close-btn");

// Add event listener to close button
closeBtn.addEventListener("click", () => {
    // Reload the website
    location.reload(true);
});

// go back
function goBack() {
    window.history.back();
}

