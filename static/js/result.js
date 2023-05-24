/*for result.html*/
function fillInputPlaceholder(selector) {
    let element = document.getElementById('formGroupExampleInput'); //input tag in which placeholder will be filled (user will input the id value in this input tag)
    const label = document.getElementById('id-descriptor-label'); /* label above the input tag (to write ID value) to describe to enter ID value*/
    if (selector.value != '') {
        let value = selector.value;
        if (value === 'registrationNo') {
            label.innerText = "Enter Registration Number";
            element.placeholder = 'Registration Number';
            element.type = 'text';
            element.addEventListener('input', () => {
                element.value = element.value.toUpperCase();
            })
        }
        else if (value === 'examRoll') {
            label.innerText = "Enter Exam Roll Number";
            element.placeholder = 'Exam Roll';
            element.type = 'number';
            element.min = 1;
            element.max = ""; /*No limit of max value*/
        }
        else if (value === 'classRoll') {
            label.innerText = "Enter Class Roll Number";
            element.placeholder = 'Class Roll';
            element.type = 'number';
            element.min = 1;
            element.max = 60;
        }
    }
    else {
        label.innerText = "Enter ID Value";
        element.placeholder = 'Registration Number / Exam Roll Number / Class Roll Number';
    }

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

/**Global data related to downloading result as pdf*/
var contentForPDF = "No Content Available";
var credentialsObjSentToServer = {}; /*To store credentials sent to server to get result*/
document.getElementById('download-as-pdf-button').addEventListener('click', () => {
    let refactoredContent = refactorContent(contentForPDF);
    // console.log(refactoredContent)

    /*For file name*/
    let fileName;
    if (credentialsObjSentToServer != {}) {
        fileName = fetchNameFromContent(refactoredContent) + ' (Session: ' + credentialsObjSentToServer.session + ' Semester: ' + credentialsObjSentToServer.semester + ' ' + credentialsObjSentToServer.idName + ': ' + credentialsObjSentToServer.idValue + ')';
    }
    downloadAsPdf(refactoredContent, fileName);
}); /*event listener for button to download result as pdf*/
/** 
 * we have removed adding event listener after getting response because due to this in every successful request, event listener is added again causing multiple event listeners for same event and cause execution of callback multiple times.
 * we can also use another method that: remove event listener when a new request made by client to server and add event listener when response is received with status code 200.
 *      - But we can't do so if callback is an anonymous function because remove event listener will not work in that case.
 *      - So, we have to use normal function and for this we have to use a global variable for content of callback function (because we can't pass arguments to callback function if it's not an anonymous function)
 * Now we are using a global variable for that purpose.
 * Then it's not a better idea to remove and add event listener every time (in each request and response).
 * So, we have use a global variable and add single event listener for that purpose (in above code).
 */


/*function to display result or error message after making request to server using ajax*/
function displayResult() {

    obj = credentialsObjSentToServer = checkInput();
    console.log(obj);
    if (obj) {
        hideWarning();/*hiding warning after successful submission.*/
        const resultContainer = document.getElementById('result-container'); /*div to display result*/
        const loadingSvg = `<center><img src="static/gif/ball.svg" alt="Loading"><center>`;
        resultContainer.innerHTML = loadingSvg; /*display loading svg*/
        const downloadAsPdfButton = document.getElementById('download-as-pdf-button'); /*button to download result as pdf*/
        downloadAsPdfButton.style.display = 'none'; /*hiding download button while request is being made to server. It will be displayed only if request is successful with status code 200.*/

        request = new XMLHttpRequest();
        if (location.hostname == '127.0.0.1')
            request.open('POST', 'http://127.0.0.1:5000/api/display-result', true);
        else
            request.open('POST', 'https://rdsbca.pythonanywhere.com/api/display-result', true);

        request.setRequestHeader('Content-Type', 'application/json');

        delete obj.isAllSelected;
        request.send(JSON.stringify(obj))

        /*hiding message div containing message about how to view the paper tittle*/
        hideMessageToViewPaperTitle();

        /*onload callback function*/
        request.onload = () => {
            if (request.status == 200) {
                /*request.responseText = request.responseText.replace("examRoll", "Exam Roll") // not work because request.responseText is read only.*/
                /*console.log(request.responseText)*/
                let responseText = request.responseText.replace("ExamRoll", "Exam Roll");
                responseText = responseText.replace("ClassRoll", "Class Roll");
                responseText = responseText.replace("TotalMarks", "Total Marks");
                responseText = responseText.replace("ResultStatus", "Result Status");
                responseText = responseText.replace("RegistrationNo", "Registration Number");
                resultContainer.innerHTML = responseText;
                downloadAsPdfButton.style.display = 'block';
                contentForPDF = responseText;

                /*if response text contains paper-code/paper-title then display message to view paper's title*/
                if (responseText.search("paper-code") != -1)
                    displayMessageToViewPaperTitle();
                /*console.log(request.responseText)*/
            }
            // else if (request.status == 400) {
            else {
                resultContainer.innerHTML = request.responseText;
                downloadAsPdfButton.style.display = 'none';

                contentForPDF = request.responseText; /*updating the content for PDF with response text received from the server*/
                /*
                 * In above line we have updated the contentForPDF global variable with current content received from the server which is not result because status code is other than 200.
                 * This is not necessary but:
                 * By the way button to download pdf ('downloadAsPdfButton') is invisible then also we are updating content for pdf.
                 * It may be used if visibility changes via dev tools or other way.
                 * If we don't update the contentForPDF with responseText (in case of response code other than 200) and button is visible (by any way) then
                    * if it's first result check on the page then contentForPDF contains "No Content Available" and file name will save with leading "Invalid Credentials <current_request_credentials>". And here, there is no issue.
                    * if there will any previous successful request and result received from server (with status code 200) then contentForPDF contains content of last result (received when request was successful and response code was 200) and file name will save with leading "RESULT FOR <student_name_from_last_successful_result> <current_request_credentials>". This is the problem.
                        * In this case, pdf contains result of last successful request (having server response code = 200) and file name contains mixture of both result of last successful request and current request.
                        * Here, request is not successful then pdf must not need to contains result but pdf contains a result.
                        * But we don't want so.
                 * That's why we are updating the contentForPDF with the responseText irrespective of response code received from the server.
                 * Due to this everything will work as expected and pdf will also contains response text received from the server.
                 */
            }
            /*
            else {
                resultContainer.innerHTML = `<div class="alert alert-danger" role="alert" style="width:80%; margin:auto;padding:auto; margin-bottom:2%; padding:0.5%; text-align:center;">Something Went Wrong. Error Code 1200</div>`
                downloadAsPdfButton.style.display = 'none';
            }
            */
        }
    }
    else {
        displayWarning();/*displaying warning because submit button is clicked without filling all the desired fields.*/
    }
}
/***********Script to download result div as PDF using library jspdf************/
/**
 * @description: function to create result div as pdf 
 * @param {string} content - HTML text content to be downloaded as PDF. Default to contentForPDF (global variable).
 * @param {string} fileName - file name for the PDF to be downloaded (without extension). Default to 'result'. 
 */
function downloadAsPdf(content = contentForPDF, fileName = "result") {
    /*fetching date and time to add in pdf*/
    let dateTime = new Date();
    const date = dateTime.toDateString(); /*readable date*/
    const time = dateTime.toLocaleTimeString(); /*readable time*/
    dateTime = date + " " + time; /*concatenating both date and time*/

    pdf = new window.jsPDF("p", "px", "a4"); /*instantiating jsPDF. We can also use jsPDF direct without using window... because window attributes are default accessible.*/
    pdf.text(x = 10, y = 20, dateTime); /*header text*/
    pdf.fromHTML(HTML = content, x = 60, y = 30); /*content text*/
    /*footer texts*/
    pdf.text(x = 10, y = 620, window.location.href, { align: "left" });
    pdf.text(x = 420, y = 620, "Page 01", { align: "right" });

    pdf.save(`${fileName}.pdf`); /*saving pdf*/
}

/**
 * @description: Function to refactor content to create interactive and user friendly pdf.
 *              - This function is written as per current response received from server on successful request (status code 200).
 * @param {string} content: HTML content received from server and to be save as PDF.
 * @returns {string} refactored HTML content.
 */
function refactorContent(content) {
    /*creating another table for top row for better visibility because it has only one column*/
    content = content.replace('<th></th>', '');
    content = content.replace('<thead>', '<tr>');
    content = content.replace('</thead>', '</tr> </table> <table>');

    /*fetching trailing string of semester like st, nd, rd and th for 1, 2, 3 and rest.. respectively.*/
    const trailingSemesterStringIndex = content.search('[snrt][tdh]</sup>');
    const trailingSemesterString = content.substring(trailingSemesterStringIndex, trailingSemesterStringIndex + 2);
    console.log(trailingSemesterString);

    /*removing superscript (dynamic content (st/nd/rd/th)) using regex because it's not working well in pdf*/
    const re = RegExp('<sup style="margin:-3px"> [snrt][tdh]</sup>');
    content = content.replace(re, trailingSemesterString);
    //console.log(content);
    return content;
}

/**
 * 
 * @param {string} content: HTML content. 
 * @returns: Name if found in the HTML content else return "Invalid".
 */
function fetchNameFromContent(content) {
    /*name is written in "<th><strong>DETAILS OF SURAJ KUMAR GIRI</strong></th>"*/
    let start = content.search('DETAILS OF ')
    if (start != -1) {
        start += "DETAILS OF ".length
    }
    const end = content.search('</strong>')

    /*if name found in the content. Means request is successful*/
    if (start != -1 && end != -1) {
        return "RESULT OF " + content.substring(start, end);
    }
    return "Invalid Credentials"; /*name not found*/
}

/**
 * function to toggle display the pop-up div stating the subject title (if available).
 * @param {String} element: Element below pop need to be displayed or removed.
 * @param {boolean} isCalledBySetTimeout: To check if this function is called by setTimeout callback or not. Default to false.
 */
function toggleSubjectTitlePopUp(element, isCalledBySetTimeout = false) {
    /*checking if popup div already exists or not */
    const existingPopUp = element.firstElementChild;
    let isPopUpExists = false; /*to check pop up exists or not*/
    try {
        if (existingPopUp.className == 'pop-up') {
            isPopUpExists = true;
        }
    }
    catch (e) {
        console.log(e)
    }
    if (isPopUpExists) {
        /*removing the existing popup*/
        existingPopUp.classList.replace('pop-up', 'remove-pop-up');
        setTimeout(() => {
            existingPopUp.remove();
        }, 500);
    }
    else {
        /**
         ** creating the new popup only if user click (not by callback of setTimeout)
         * checking using isCalledBySetTimeout is necessary because we are calling the function 3s after creating the popup.
         * But if user click on the subject title within 3s then pop will be removed and then callback will be called and popup will be created again.
         * Due to this, we have taken a new variable isCalledBySetTimeout to check if this function is called by setTimeout callback or not.
         * If it's called by setTimeout callback then we will not create the popup again.
         * If it's called by user click and popup doesn't exists then we will create the popup.
         * * So, to avoid creating the popup again and again without user interaction, we have used isCalledBySetTimeout.
         * * Means we are simply restricting the callback to create the popup. popup can be created by user interaction only.
        */
        if (!isCalledBySetTimeout) {
            const div = document.createElement("div");
            div.textContent = element.title; /*subject title as div textContent */
            div.className = "pop-up";
            element.appendChild(div);
            setTimeout(() => { toggleSubjectTitlePopUp(element, true) }, 3000); /*removing the popup after 3 seconds. */
        }
    }
}


/**
 * We have given functionality to view the paper title by clicking/hover on the paper-code.
 * But user don't know about the functionality. That's why, a note will be display to inform the user about the same.
 * Below two functions are related to display the message or hide the message.
 */

const displayMessageToViewPaperTitle = () => {
    if (!document.getElementById('note-message-container')) {
        const noteMessageDiv = document.createElement("div");
        noteMessageDiv.id = "note-message-container";
        noteMessageDiv.innerHTML = `<div class="alert alert-primary" role="alert">
                                <b>Note</b>: Click ${window.screen.width > 768 ? ' or hover' : ''} on paper code to view the paper title.
                                <a href="javascript:void(0)"> Click here to toggle view all</a>
                                </div>`;
        noteMessageDiv.firstElementChild.style.cssText = `width: 80%; padding: auto; margin: auto; padding: 0.3%; text-align: center;`
        noteMessageDiv.firstElementChild.lastElementChild.addEventListener('click', () => {
            const paperCodeTds = document.querySelectorAll(".paper-code");
            for (let element of paperCodeTds) {
                element.click();
            }
        })
        noteMessageDiv.style = "margin-bottom: 1%;";
        document.body.insertBefore(noteMessageDiv, document.getElementById("download-as-pdf-button").nextElementSibling);
    }
    else {
        document.getElementById('note-message-container').style.display = "block";
    }
}

const hideMessageToViewPaperTitle = () => {
    if (document.getElementById('note-message-container')) {
        document.getElementById('note-message-container').style.display = "none";
    }
}