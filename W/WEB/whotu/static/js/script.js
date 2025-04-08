document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("#login-form");
    const signupForm = document.querySelector("#signup-form");

    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();
            alert("Logging in... (Replace this with backend handling)");
        });
    }

    if (signupForm) {
        signupForm.addEventListener("submit", function (e) {
            e.preventDefault();
            alert("Signing up... (Replace this with backend handling)");
        });
    }
    
    // Toggle premium content alert
    const premiumLink = document.querySelector("#premium-link");
    if (premiumLink) {
        premiumLink.addEventListener("click", function (e) {
            e.preventDefault();
            alert("Accessing premium content! Ensure authentication is set up.");
        });
    }
});
