"use strict";

function reset() {
    const inputElements = document.getElementsByTagName('input');
    for (let i = 0; i < inputElements.length; i++) {
        inputElements[i].value = '';
    }
}

/*function to add +91 before mobile number if there is no value.*/
function leading91(element) {
    if (element.value == "")
        element.value = "+91 ";
}

/*To fetch student details from database (from server) if exist (after filling the registration field in HTML form)*/
/*ids
 *floatingInputGroup1 for registration field
 *floatingInputGroup2 for firstName field
 *floatingInputGroup3 for lastName field
 *floatingInputGroup7 for examRollNumber field
 *floatingInputGroup8 for classRollNumber field
 *floatingSelect for session field
 */
const regElement = document.getElementById('floatingInputGroup1'); /*registrationNo input element*/
regElement.addEventListener('change', checkInDatabase);

/*converting the desired input to uppercase*/
/*1. registration Number*/
regElement.addEventListener('input', () => { regElement.value = regElement.value.toUpperCase() });

/*2. First Name*/
let firstName = document.getElementById('floatingInputGroup2');
firstName.addEventListener('input', () => firstName.value = firstName.value.toUpperCase());

/*3. Last Name*/
let lastName = document.getElementById('floatingInputGroup3');
lastName.addEventListener('input', () => lastName.value = lastName.value.toUpperCase());


/*function to check if the registration number is already in database. If yes, then fill the other fields automatically by fetching the details using API from server (HTTP request)*/
function checkInDatabase() {
    const regNo = regElement.value;
    if (regNo.length < 10)
        return;

    let url;
    if (window.location.href.includes('127.0.0.1'))
        url = 'http://127.0.0.1:5000/getDetails/' + regNo;
    else
        url = 'https://rdsbca.pythonanywhere.com/getDetails/' + regNo;
    showEdgeLoading();
    fetch(url)
        .then(response => response.json())
        .then(data => {
            hideEdgeLoading();
            if (data != null) {
                console.log(data)
                const nameArray = data.name.split(' ');
                console.log(nameArray);
                const restName = nameArray.slice(1).join(' ');

                document.getElementById('floatingInputGroup2').value = nameArray[0];
                document.getElementById('floatingInputGroup3').value = restName;
                document.getElementById('floatingInputGroup7').value = data.examRoll;
                document.getElementById('floatingInputGroup8').value = data.classRoll;
                document.getElementById('floatingSelect').value = data.session;
            }
            else {
                document.getElementById('floatingInputGroup2').value = "";
                document.getElementById('floatingInputGroup3').value = "";
                document.getElementById('floatingInputGroup7').value = "";
                document.getElementById('floatingInputGroup8').value = "";
                document.getElementById('floatingSelect').value = "";
            }
        })
}


/*function to show and hide edge loading animation while fetching data from server using API (using registration number) */
function hideEdgeLoading() {
    const element = document.getElementById('edge-loading');
    element.style.display = 'none';
}

function showEdgeLoading(type = 'block') {
    const element = document.getElementById('edge-loading');
    element.style.display = type;
}