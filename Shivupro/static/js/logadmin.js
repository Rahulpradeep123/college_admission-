function promptForAdminPassword() {
    var password = prompt("Enter admin password:");
    if (password === "Rahul") {
        window.location.href = "/admin_login"; 
    } else {
        alert("Incorrect password. Access denied.");
    }
}


