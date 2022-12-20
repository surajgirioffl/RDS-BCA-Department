"userStrict"

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

function checkInDatabase() {
    const regNo = regElement.value;
    const url = 'http://127.0.0.1:5000/getDetails/' + regNo;
    fetch(url)
        .then(response => response.json())
        .then(data => {
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