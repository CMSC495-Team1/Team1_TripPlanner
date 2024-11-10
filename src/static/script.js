const selection = document.getElementById('statesinalist');
const statetexts = Array.from(document.getElementsByClassName('state-name-text'));
const flightButton = document.getElementById('flightbutton');
const hotelButton = document.getElementById('hotelbutton');
const carButton = document.getElementById('carbutton');
const startPlanningButton = document.getElementById('startplanningbutton');
const navBar = document.getElementById('topnav');
var userName = "username";
var flightButtonActive = false;
var hotelButtonActive = false;
var carButtonActive = false;
var startPlanningActive = false;


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
    var isClickInside = (submenu.contains(event.target) || userButton.contains(event.target));
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
    var isClickInside = (contactContainer.contains(event.target) || contactButton.contains(event.target));
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
    var isClickInside = (loginmenu.contains(event.target) || loginButton.contains(event.target));
    if (!isClickInside && loginmenu.classList.contains("open-menu")) {
        loginmenu.classList.remove("open-menu");
    }
});

//changes text related to the selected state on Plan Trips
function changeState() {
    var text = selection.options[selection.selectedIndex].text;
    statetexts.forEach(element => {
        element.innerHTML = text;
    });
}

//when selecting trip types on Plan Trip, causes them to be highlighted and records it in a boolean
function changeTrip(tripType) {
    if (tripType === "car") {
        if (carButtonActive == true) {
            carButtonActive = false;
            carButton.style.border = "none";
        }
        else {
            carButtonActive = true;
            carButton.style.border = "2px solid yellow";
        }
    }
    else if (tripType === "hotel") {
        if (hotelButtonActive == true) {
            hotelButtonActive = false;
            hotelButton.style.border = "none";
        }
        else {
            hotelButtonActive = true;
            hotelButton.style.border = "2px solid yellow";
        }
    }
    else if (tripType === "flight") {
        if (flightButtonActive) {
            flightButtonActive = false;
            flightButton.style.border = "none";
        }
        else {
            flightButtonActive = true;
            flightButton.style.border = "2px solid yellow";
        }
    }
    if (flightButtonActive || hotelButtonActive || carButtonActive) {
        startPlanningButton.style.backgroundColor = "blue";
        startPlanningActive = true;
    }
    else {
        startPlanningButton.style.backgroundColor = "gray";
        startPlanningActive = false;
    }
}

//functionality needs ot be added to book whatever is active from here.
function startPlanning() {
    if (startPlanningActive) {
        alert("Start planning active!");
    }
    else {
        alert("Start planning NOT active!");
    }
}


//Used to create the navigation bar at the top of the page. differs depending on whether a user is logged in or not.
function displayNavBar() {
    if (userName != "") {
        navBar.innerHTML = "<a href='/'><img src='/static/images/banner.png' alt='Team 1 Travel Planner banner'"
            + "width='961' height='51'></a> <button class='button signup' id='usernameButton' onclick='toggleMenu();'>" + userName + "</button>"
            + "<div id='submenu-container'><div id='submenu'><a href='/view_trips'><button class='submenu-button'>View Trips</button></a>"
            + "<a href='/account_settings'><button class='submenu-button'>Account Settings</button></a>"
            + "<button class='submenu-button' onclick='logOut();'>Log Out</button></div></div>";
    }
    else {
        navBar.innerHTML = "<a href='/'><img src='/static/images/banner.png' alt='Team 1 Travel Planner banner'"
            + "width='961' height='51'></a> <a href='/sign_up'><button class='button signup'>SIGN UP</button></a> "
            + "<button class='button login' id='login-button' onclick='toggleLoginMenu();'>LOGIN</button>"
            + "<div id='loginmenu-container'><div id='loginmenu'><div class='plan-form'><form id='tripForm'><table id='logintable'>"
            + "        <tr><td>User ID:</td><td><input type='text' id='userID' required></td></tr>"
            + "        <tr><td>Password:</td><td><input type='password' id='password' required></td></tr>"
            + "    </table><button type='submit'>Submit</button></form><br><a href='/forgotpassword'>Forgot password? Click here.</a></div></div></div>";
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
}
//simple log in action. temporary
function logIn() {
    userName = "username";
    displayNavBar();
}


selection.addEventListener('change', changeState);