const navBar = document.getElementById('topnav');
let userName = "";




//To open and close the user menu
let submenu = document.getElementById("submenu-container");
let userButton = document.getElementById("usernameButton");

function toggleMenu() {
    submenu = document.getElementById("submenu-container");
    submenu.classList.toggle("open-menu");
}

document.addEventListener('click', function (event) {
    submenu = document.getElementById("submenu-container");
    userButton = document.getElementById("usernameButton");
    let isClickInside = (submenu.contains(event.target) || userButton.contains(event.target));
    if (!isClickInside && submenu.classList.contains("open-menu")) {
        submenu.classList.remove("open-menu");
    }
});

//To open and close the contact window
let contactContainer = document.getElementById("subcontact");
let contactButton = document.getElementById("contact-button");

function toggleContactInfo() {
    contactContainer.classList.toggle("open-menu");
}

document.addEventListener('click', function (event) {
    let isClickInside = (contactContainer.contains(event.target) || contactButton.contains(event.target));
    if (!isClickInside && contactContainer.classList.contains("open-menu")) {
        contactContainer.classList.remove("open-menu");
    }
});

//To open and close the login window
let loginmenu = document.getElementById("loginmenu-container");
let loginButton = document.getElementById("login-button");


function toggleLoginMenu() {
    loginmenu = document.getElementById("loginmenu-container");
    loginmenu.classList.toggle("open-menu");
}

document.addEventListener('click', function (event) {
    loginmenu = document.getElementById("loginmenu-container");
    loginButton = document.getElementById("login-button");
    let isClickInside = (loginmenu.contains(event.target) || loginButton.contains(event.target));
    if (!isClickInside && loginmenu.classList.contains("open-menu")) {
        loginmenu.classList.remove("open-menu");
    }
});





function logOut() {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            if (response.ok) {
                userName = "";
                displayNavBar();
                const currentUrl = window.location.href;
                if (currentUrl.includes("account_settings") || currentUrl.includes("view_trips")) {
                    location.href = "/";
                }
            } else {
                console.error('Logout failed');
            }
        })
        .catch(error => console.error('Error:', error));
}
