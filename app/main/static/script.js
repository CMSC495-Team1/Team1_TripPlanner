const navBar = document.getElementById('topnav');
let userName = "";
let userFirstName = "";

// Check initial login state
fetch('/check_login', {
    method: 'GET',
    credentials: 'same-origin'
})
.then(response => {
    if (response.ok) {
        response.text().then(data => {
            if (data) {
                const [firstName, username] = data.split(':');
                userFirstName = firstName;
                userName = username;
                displayNavBar();
            }
        });
    }
});

displayNavBar();

// User submenu handling
let submenu = document.getElementById("submenu-container");
let userButton = document.getElementById("usernameButton");

function toggleMenu() {
    submenu = document.getElementById("submenu-container");
    submenu.classList.toggle("open-menu");
}

document.addEventListener('click', function (event) {
    submenu = document.getElementById("submenu-container");
    userButton = document.getElementById("usernameButton");
    let isClickInside = (submenu && userButton) ? (submenu.contains(event.target) || userButton.contains(event.target)) : false;
    if (!isClickInside && submenu && submenu.classList.contains("open-menu")) {
        submenu.classList.remove("open-menu");
    }
});

// Login menu handling
let loginmenu = document.getElementById("loginmenu-container");
let loginButton = document.getElementById("login-button");

function toggleLoginMenu() {
    loginmenu = document.getElementById("loginmenu-container");
    loginmenu.classList.toggle("open-menu");
}

document.addEventListener('click', function (event) {
    loginmenu = document.getElementById("loginmenu-container");
    loginButton = document.getElementById("login-button");
    let isClickInside = (loginmenu && loginButton) ? (loginmenu.contains(event.target) || loginButton.contains(event.target)) : false;
    if (!isClickInside && loginmenu && loginmenu.classList.contains("open-menu")) {
        loginmenu.classList.remove("open-menu");
    }
});

function handleLoginSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);

    fetch('/login', {
        method: 'POST',
        body: formData,
        credentials: 'same-origin'
    })
    .then(response => {
        if (response.ok) {
            response.text().then(data => {
                const [firstName, username] = data.split(':');
                userFirstName = firstName;
                userName = username;
                displayNavBar();
                window.location.href = '/plan_trip';
            });
        } else if (!response.ok) {
            response.text().then(error => {
                const errorDiv = document.getElementById('login-error') || createErrorDiv();
                errorDiv.textContent = error;
            });
        }
    })
    .catch(error => {
        const errorDiv = document.getElementById('login-error') || createErrorDiv();
        errorDiv.textContent = 'An error occurred. Please try again.';
    });
}

function createErrorDiv() {
    const existingError = document.getElementById('login-error');
    if (existingError) {
        existingError.remove();
    }

    const errorDiv = document.createElement('div');
    errorDiv.id = 'login-error';
    errorDiv.style.color = '#87CEEB';
    const formContainer = document.getElementById('login-form-container');
    formContainer.insertBefore(errorDiv, formContainer.firstChild);
    return errorDiv;
}

function logOut() {
    fetch('/logout', {
        method: 'GET',
        credentials: 'same-origin'
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;  // Follow the server's redirect
        } else if (response.ok) {
            userName = "";
            userFirstName = "";
            displayNavBar();
        }
    });
}

function displayNavBar() {
    if (userName !== "") {
        navBar.innerHTML = "<a href='/'><img src='" + banner_url + "' alt='Team 1 Travel Planner banner'"
            + " width='961' height='51'></a> <button class='button signup' id='usernameButton'"
            + " onclick='toggleMenu();'>" + userFirstName + "</button>"
            + "<div id='submenu-container'><div id='submenu'><a href='/view_trips'><button class='submenu-button'>View Trips</button></a>"
            + "<a href='/account_settings'><button class='submenu-button'>Account Settings</button></a>"
            + "<button class='submenu-button' onclick='logOut();'>Log Out</button></div></div>";
    } else {
        navBar.innerHTML = "<a href='/'><img src='" + banner_url + "' alt='Team 1 Travel Planner banner'"
            + " width='961' height='51'></a> <a href='/sign_up'><button class='button signup'>SIGN UP</button></a> "
            + "<button class='button login' id='login-button' onclick='toggleLoginMenu();'>LOGIN</button>"
            + "<div id='loginmenu-container'><div id='loginmenu'><div class='plan-form' id='login-form-container'>"
            + "Loading...</div></div></div>";

        // Fetch the login form HTML
        fetch('/login_form')
            .then(response => response.text())
            .then(html => {
                document.getElementById('login-form-container').innerHTML = html;
                const loginForm = document.getElementById('loginForm');
                if (loginForm) {
                    loginForm.addEventListener('submit', handleLoginSubmit);
                }
            });
    }
}

// Add event listener after navbar is rendered
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLoginSubmit);
    }
});
