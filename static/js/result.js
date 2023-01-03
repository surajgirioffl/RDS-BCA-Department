/*for result.html*/
function fillInputPlaceholder(selector) {
    let element = document.getElementById('formGroupExampleInput');
    if (selector.value != '') {
        let value = selector.value;
        if (value === 'registrationNo')
            element.placeholder = 'Registration Number';
        else if (value === 'examRoll')
            element.placeholder = 'Exam Roll';
        else if (value === 'classRoll')
            element.placeholder = 'Class Roll';
    }
    else
        element.placeholder = 'Registration Number / Exam Roll Number / Class Roll Number';

}

/*function to display warning if all the options are not selected*/
function displayWarning() {
    const warningDiv = document.getElementById('warning'); /*div to display warning*/

    /*if waring div is not present then create it*/
    if (warningDiv == null) {
        const warningDiv = document.createElement('div');
        warningDiv.innerHTML = `<div id="warning">All fields are mandatory.</div>`;
        warningDiv.style.animationName = 'slide-right';
        warningDiv.style.animationDuration = '1s';
        const form = document.getElementsByTagName('form')[0];

        /*inserting before first child of form. Making the warning div the first child of form*/
        form.insertBefore(warningDiv, form.firstElementChild);
    }
    warningDiv.style.animationName = 'slide-right';
    warningDiv.style.animationDuration = '1s';
    warningDiv.style.display = 'block';
}

/*function to hide warning if all the options are selected*/
function hideWarning() {
    const warningDiv = document.getElementById('warning');
    if (warningDiv != null) {
        warningDiv.style.animationName = 'slide-left';
        warningDiv.style.animationDuration = '1s';
        setTimeout(() => { warningDiv.style.display = 'none' }, 1000);
    }
}


/***************To display result***********************/
/*document.getElementsByTagName('form')[0].onsubmit = "return false;"; //It will work in html because it has more priority. But not here because it is suppressed by displayResult() function called on click event of submit button. . So, I have to use preventDefault() method.*/
document.getElementsByTagName('form')[0].addEventListener('submit', function (event) { event.preventDefault(); });
var submitButton = document.getElementById('submit-button');
submitButton.addEventListener('click', displayResult); /*this will suppress the default behavior of submit button. 'required' will not behave as expected because more than one EventListeners are set for same event. And this lister will work first. So, 'required' will work after it. So, we will have to check if all the options are selected or not.*/

/*function to check if all the options are selected*/
function checkInput() {
    try {
        const session = document.querySelector('select[name="session"]');
        const semester = document.querySelector('select[name="semester"]');
        const idName = document.querySelector('select[name="idName"]');
        const idValue = document.querySelector('input[name="idValue"]');
        if (session.value != '' && semester.value != '' && idName.value != '' && idValue.value != '') {
            return { isAllSelected: true, session: session.value, semester: semester.value, idName: idName.value, idValue: idValue.value }
        }
        throw new Error('Please select all the options.\nAll fields are mandatory.');
    }
    catch (error) {
        console.log(error.message)
    }
    return false;

}

/*function to display result or error message after making request to server using ajax*/
function displayResult() {

    obj = checkInput();
    console.log(obj);
    if (obj) {
        hideWarning();/*hiding warning after successful submission.*/
        const resultContainer = document.getElementById('result-container'); /*div to display result*/
        const loadingSvg = `<center><img src="static/gif/ball.svg" alt="Loading"><center>`;
        resultContainer.innerHTML = loadingSvg; /*display loading svg*/

        request = new XMLHttpRequest();
        if (location.hostname == '127.0.0.1')
            request.open('POST', 'http://127.0.0.1:5000/api/display-result', true);
        else
            request.open('POST', 'https://rdsbca.pythonanywhere.com/api/display-result', true);

        request.setRequestHeader('Content-Type', 'application/json');

        delete obj.isAllSelected;
        request.send(JSON.stringify(obj))

        /*onload callback function*/
        request.onload = () => {
            if (request.status == 200) {
                /*request.responseText = request.responseText.replace("examRoll", "Exam Roll") // not work because request.responseText is read only.*/
                /*console.log(request.responseText)*/
                let responseText = request.responseText.replace("examRoll", "Exam Roll");
                responseText = responseText.replace("classRoll", "Class Roll");
                responseText = responseText.replace("TotalMarks", "Total Marks");
                responseText = responseText.replace("ResultStatus", "Result Status");
                resultContainer.innerHTML = responseText;
                /*console.log(request.responseText)*/
            }
            else {
                resultContainer.innerHTML = `<div class="alert alert-danger" role="alert" style="width:80%; margin:auto;padding:auto; margin-bottom:2%; padding:0.5%; text-align:center;">Something Went Wrong. Error Code 1200</div>`
            }
        }
    }
    else {
        displayWarning();/*displaying warning because submit button is clicked without filling all the desired fields.*/
    }
}