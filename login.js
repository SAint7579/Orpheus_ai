document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
  
    if (username === "test" && password === "test") {
      document.getElementById("message").textContent = "Login successful!";
      window.location.href = "page2.html"; // Redirect to page2.html
    } else {
      document.getElementById("message").textContent = "Invalid username or password.";
    }
  });
  