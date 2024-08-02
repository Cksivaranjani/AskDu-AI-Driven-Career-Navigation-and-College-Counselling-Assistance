const navbarMenu = document.querySelector(".navbar .links");
const hamburgerBtn = document.querySelector(".hamburger-btn");
const hideMenuBtn = navbarMenu.querySelector(".close-btn");


// Show mobile menu
hamburgerBtn.addEventListener("click", () => {
    navbarMenu.classList.toggle("show-menu");
});
// Hide mobile menu
hideMenuBtn.addEventListener("click", () =>  hamburgerBtn.click());


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



// download popup
const showdownPop = document.querySelector(".download");

const downloadPopup = document.querySelector(".download-popup");

showdownPop.addEventListener("click", () => {
    document.body.classList.toggle("show-downpopup");
});

const hidedownPop = document.querySelector(".download-popup .close-btn");
hidedownPop.addEventListener("click", () => showdownPop.click());


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

function sendMessage() {
    var userInput = document.getElementById("message").value.trim();
    console.log("User input:", userInput);
    if (userInput !== "") {
        addUserMessage(userInput);
        sendUserMessage(userInput);
        document.getElementById("message").value = "";
    }
}

function addUserMessage(message) {
    var conversation = document.getElementById("conversation");
    var sentMessageDiv = document.createElement("div");
    sentMessageDiv.className = "sent-message";
    sentMessageDiv.innerHTML = `
        <div class="sender-info">
            <span>User</span>
            <i class="fas fa-user"></i>
        </div>
        <div class="message sent">
            <div class="message-text">${message}</div>
        </div>`;
    conversation.appendChild(sentMessageDiv);
}

function addBotMessage(message) {
    var conversation = document.getElementById("conversation");
    var receivedMessageDiv = document.createElement("div");
    receivedMessageDiv.className = "received-message";
    receivedMessageDiv.innerHTML = `
        <div class="receiver-info">
            <img src="./static/Screenshot (377).png" alt="Bot Image">
            <span>AskDu</span>
        </div>
        <div class="message received">
            <div class="message-text">${message}</div>
        </div>`;
    conversation.appendChild(receivedMessageDiv);
}

function sendUserMessage(message) {
    var formData = new FormData();
    formData.append("message", message);

    fetch("/send-message", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                var botMessages = data.bot_messages;
                botMessages.forEach(message => addBotMessage(message));
            } else {
                console.error("Error sending user message:", data.error);
            }
        })
        .catch(error => {
            console.error("Error sending user message:", error);
        });
}

// Initial bot greeting
// document.addEventListener("DOMContentLoaded", function() {
//     addBotMessage("Welcome to AskDu! How can I assist you today?");
// });

// to add download content
function addMessageToDownloadContent(message, messageType) {
    var downloadContent = document.getElementById("pdf-content");
    var messageDiv = document.createElement("div");
    
    if (messageType === 'user') {
        messageDiv.className = "sent-message";
    } else if (messageType === 'bot') {
        messageDiv.className = "received-message";
    }
    
    messageDiv.innerHTML = `
        <div class="message-text">${message}</div>`;
    
    downloadContent.appendChild(messageDiv);
}
function sendUserMessage(message) {
    var formData = new FormData();
    formData.append("message", message);

    fetch("/send-message", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                var botMessages = data.bot_messages;
                botMessages.forEach(message => {
                    addBotMessage(message);
                    addMessageToDownloadContent(message, 'bot');
                });
            } else {
                console.error("Error sending user message:", data.error);
            }
        })
        .catch(error => {
            console.error("Error sending user message:", error);
        });
}
