// // script.js
// const socket = io.connect('http://127.0.0.1:5000');

// // Listen for document updates
// socket.on('document_update', function (message) {
//     console.log('Received update:', message);
//     // You can update the DOM with the message or refresh content here
//     document.getElementById('documentContent').innerText = message;
// });

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const documentContent = document.getElementById("document-content");

    // Create a Bootstrap alert for success (initially hidden)
    const alertBox = document.createElement("div");
    alertBox.className = "alert alert-success";
    alertBox.id = "alert-box";
    alertBox.role = "alert";
    alertBox.style.display = "none"; // Initially hidden
    document.body.prepend(alertBox); // Add to the top of the page

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent page navigation

        // Get form data
        const formData = new FormData(form);

        // Send form data using Fetch API (AJAX)
        fetch("/edit", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Show success alert
            alertBox.innerHTML = "✅ Changes Saved Successfully!";
            alertBox.style.display = "block"; // Show the alert

            // Auto-hide the alert after 3 seconds
            setTimeout(() => {
                alertBox.style.display = "none";
            }, 3000);

            // Update document content with new changes
            if (data.user && data.message) {
                let newEntry = document.createElement("p");
                newEntry.innerHTML = `<strong>${data.user}:</strong> ${data.message}`;
                documentContent.appendChild(newEntry);
            }
        })
        .catch(error => console.error("Error:", error));
    });

    // Real-time updates with Socket.io
    const socket = io.connect('http://127.0.0.1:5000');

    socket.on('document_update', function (message) {
        console.log('Received update:', message);

        if (message.user && message.text) {
            let updatedEntry = document.createElement("p");
            updatedEntry.innerHTML = `<strong>${message.user}:</strong> ${message.text}`;
            documentContent.appendChild(updatedEntry);
        }
    });
});
