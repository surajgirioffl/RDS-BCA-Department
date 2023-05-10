/*if user changes any attributes using devtools then following will be executed*/
window.addEventListener('load', () => {
    const element = document.querySelectorAll('[name=semester]')[0];
    const button = document.querySelectorAll('[type=submit]')[0];
    element.addEventListener('change', () => {
        let sameElement = document.querySelectorAll('[name=semester]')[0];
        console.log(element.value);
        if (sameElement == undefined) {
            /*means that the element is not present in the page or user change the name using devtools*/
            button.style.cursor = 'no-drop';
            button.disabled = true;
            let message = document.getElementById('myAlert');
            if (message == undefined) {
                button.parentElement.appendChild(createAlert());
            }
        }
        else {
            button.style.cursor = 'pointer';
            button.disabled = false;
            let message = document.getElementById('myAlert');
            if (message != undefined) {
                message.remove();
            }
        }
    });
});


function createAlert() {
    let alert = document.createElement('div');
    alert.className = 'alert alert-danger';
    alert.role = 'alert';
    alert.style.cssText = 'padding:0.5%; margin-top:1%; font-weight: bold;';
    alert.innerHTML = 'Changes using devtools is not allowed.';
    alert.id = 'myAlert';
    return alert;
}

/** 
 * @fetching_previous_year_questions_using_API_route
 * serving previous year questions using AJAX 
*/

window.addEventListener('load', () => {
    /*preventing default behavior of the form element which is after submitting the form page will reload and form data sent using url parameters.*/
    document.getElementsByTagName('form')[0].addEventListener('submit', (event) => {
        event.preventDefault();
        displayPreviousYearQuestions();
    })
    // document.getElementById('submit-button').addEventListener('click', displayPreviousYearQuestions);
    /**
     * Here, I have not added any event listener on submit button. So, default checking after clicking on submit button of form will work as expected.
     * Means default checking of form will work as expected.
     * But If I were added event listener on submit button then default checking of form will not work as expected.
     * Because, custom event listener will be executed first and then default checking of form will be executed.
     * And due to custom event listener, default checking of form will not work as expected.
     */
})


function displayPreviousYearQuestions() {
    document.getElementById('previous-year-questions-container').innerHTML = ''; /*cleaning the previous response/result if available*/
    document.getElementById('loading-svg').style.display = 'block';
    const request = new XMLHttpRequest();
    if (window.location.hostname == '127.0.0.1')
        request.open('POST', 'http://127.0.0.1:5000/api/fetch-previous-year-questions', async = true);
    else
        request.open('POST', 'https://rdsbca.pythonanywhere.com/api/fetch-previous-year-questions', async = true);

    request.setRequestHeader('Content-Type', 'application/json')
    const obj = { semester: document.getElementById('semester').value, source: document.getElementById('source').value };
    console.log(obj)
    request.send(JSON.stringify(obj))
    request.onload = () => {
        document.getElementById("previous-year-questions-container").innerHTML = request.responseText;
        document.getElementById('loading-svg').style.display = 'none';
        if (request.status == 200)
            initializePopovers();
    }
}

function initializePopovers() {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

    /* Adding some event listeners.
     * Like adding functionality to display only one popover at a time.
     */
    const popovers = popoverTriggerList;
    for (object of popovers) {
        object.addEventListener('click', hidePopover);
    }
}

/**
 * Function to hide the currently visible popover.
 */
var hidePopover = () => {
    const visiblePopovers = document.querySelectorAll("[aria-describedby]");
    if (visiblePopovers[0] != undefined)
        visiblePopovers[0].click(); /*Means any of the popover is visible.*/
}

/*hide the currently visible popover by clicking anywhere*/
document.addEventListener('click', hidePopover);