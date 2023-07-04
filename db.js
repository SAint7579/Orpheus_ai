document.addEventListener("DOMContentLoaded", function() {
    var insertButton = document.getElementById("insertButton");

    insertButton.addEventListener("click", function() {
        var value1 = 10;  // Replace with your desired value
        var value2 = 5;  // Replace with your desired value

        // Create a new XMLHttpRequest object
        var xhr = new XMLHttpRequest();

        // Set the request URL
        xhr.open("POST", "http://localhost:3000/insert", true);  // Replace with your server-side endpoint

        // Set the request headers
        xhr.setRequestHeader("Content-Type", "application/json");

        // Handle the response from the server
        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log(xhr.responseText);
            } else {
                console.error("Error: " + xhr.status);
            }
        };

        // Handle any errors that occur during the AJAX request
        xhr.onerror = function() {
            console.error("Request failed.");
        };

        // Send the data to the server
        var data = {
            value1: value1,
            value2: value2
        };
        xhr.send(JSON.stringify(data));
    });
});
