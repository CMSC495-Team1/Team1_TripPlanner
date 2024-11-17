const navBar = document.getElementById('topnav');
let userName = "username";


displayNavBar();


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


//Used to create the navigation bar at the top of the page. differs depending on whether a user is logged in or not.
function displayNavBar() {
    if (userName !== "") {
        navBar.innerHTML = "<a href='/'><img src=' " + banner_url + "' alt='Team 1 Travel Planner banner'"
            + " width='961' height='51'></a> <button class='button signup' id='usernameButton'" +
            " onclick='toggleMenu();'>" + userName + "</button>"
            + "<div id='submenu-container'><div id='submenu'><a href='/view_trips'><button class='submenu-button'>View Trips</button></a>"
            + "<a href='/account_settings'><button class='submenu-button'>Account Settings</button></a>"
            + "<button class='submenu-button' onclick='logOut();'>Log Out</button></div></div>";
    }
    else {
        navBar.innerHTML = "<a href='/'><img src='" + banner_url + "' alt='Team 1 Travel Planner banner'"
            + " width='961' height='51'></a> <a href='/sign_up'><button class='button signup'>SIGN UP</button></a> "
            + "<button class='button login' id='login-button' onclick='toggleLoginMenu();'>LOGIN</button>"
            + "<div id='loginmenu-container'><div id='loginmenu'><div class='plan-form'><form id='tripForm'><table id='logintable'>"
            + "        <tr><td>User ID:</td><td><input type='text' id='userID' required></td></tr>"
            + "        <tr><td>Password:</td><td><input type='password' id='password' required></td></tr>"
            + "    </table><button type='submit'>Submit</button></form><br><a href='/forgot_password'>Forgot password? Click here.</a></div></div></div>";
    }
}


//simple log out action. temporary
function logOut() {
    const currentUrl = window.location.href;
    userName = "";
    displayNavBar();
    if (currentUrl.includes("account_settings")||currentUrl.includes("view_trips")){
        location.href= "/";
    }

//simple log in action. temporary
// function logIn() {
//     userName = "username";
//     displayNavBar();
}