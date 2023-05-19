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
        /* Removing the trailing city name from the source name in the response text if screen width is less than 768px (mobile screen) for better UI.
         * Removing the city name from the response text if screen width is less than 768px (mobile screen).
         * This is done because in mobile screen, if the name of source contains city name then height of table row will increase (in more than 1 line) and it will not look good because other data in same row are just one lined.
        */
        let responseText = request.responseText
        if (window.screen.width <= 768) {
            // request.responseText = request.responseText.replaceAll(', Muzaffarpur', '');
            /* Above line will not work because request.responseText is read only*/
            responseText = responseText.replaceAll(', Muzaffarpur', '');
        }
        document.getElementById("previous-year-questions-container").innerHTML = responseText;
        document.getElementById('loading-svg').style.display = 'none';

        /* Semester 4 note starts
         * In semester system, java is added in 4th semester. But in year system, java was in 3rd year (5th sem of vaishali or ln mishra - sub code 502)
         * So, for java PYQ before 2022, we will have to display PYQ of 5th semester of vaishali or ln mishra.
         * This note will give information about this to the user.
         * So, this note will be displayed only if semester is 4.
         */
        if (obj.semester == 4) {
            if (!document.getElementById('note-message-container')) {
                const noteMessageDiv = document.createElement("div");
                noteMessageDiv.innerHTML = `<div class="alert alert-primary" role="alert">
                                        Note: In the year system, Java was in 3rd year (See Vaishali/Ln Mishra 5th sem - Sub code 502). So, for Java PYQ before 2022 
                                        <a href="javascript:void(0)"> Click here </a>
                                        </div>`;
                noteMessageDiv.firstElementChild.style.cssText = `padding: 0.3%;`
                noteMessageDiv.firstElementChild.firstElementChild.addEventListener('click', () => {
                    document.getElementById('semester').value = 5;
                    document.getElementById('source').value = 'vaishali';
                    document.getElementById('submit-button').click();
                })
                noteMessageDiv.id = "note-message-container";
                document.getElementById("previous-year-questions-container").parentElement.appendChild(noteMessageDiv);
            }
        }
        else {
            const noteMessageDiv = document.getElementById('note-message-container');
            if (noteMessageDiv) {
                /*if exists*/
                noteMessageDiv.remove();
            }
        }
        /* Semester 4 note ends */

        /*feedback starts*/
        /*User can submit feedback if any issue occurs*/
        if (!document.getElementById('feedback-div')) {
            /*if feedback div is not present then create it*/
            const feedbackDiv = document.createElement('div');
            feedbackDiv.id = 'feedback-div';
            feedbackDiv.innerHTML = `<div class="alert alert-danger" role="alert">
                                            Having any issues? <a href="https://forms.gle/F7hxnRh5TvaALRMQ8" target="_blank">Click here</a> to submit feedback
                                    </div>`
            feedbackDiv.firstElementChild.style.cssText = `padding: 0.2%;`
            document.getElementById("previous-year-questions-container").parentElement.appendChild(feedbackDiv);
        }
        /*Feedback ends*/

        if (request.status == 200) {
            initializePopovers();
            initializeViewButtons();
        }
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
        object.addEventListener("click", new Files(object.getAttribute('file-id')).displayFileMetadata);
        object.addEventListener('click', hidePopover);
    }
}

/**
 * Function to hide the currently visible popover.
 */
var hidePopover = () => {
    const visiblePopovers = document.querySelectorAll("[aria-describedby]");
    if (visiblePopovers[0] != undefined)
        bootstrap.Popover.getOrCreateInstance(visiblePopovers[0]).hide();
    /*source: https://getbootstrap.com/docs/5.2/components/popovers/*/
}

/*hide the currently visible popover by clicking anywhere*/
document.addEventListener('click', hidePopover);

/*hide the currently visible popover by pressing escape key*/
document.addEventListener('keydown', (event) => {
    console.log(event.key, "is pressed.")
    event.key == 'Escape' ? hidePopover() : null;
})

class Files {
    fileId; /*no need to write it. But explicitly writing instance variables are better for get them easily*/

    constructor(fileId) {
        this.fileId = fileId;
    }
    /*Method to fetch the metadata of the specified fileId.*/
    #fetchAndUpdateFileMetadata = () => {
        /*
         * Displaying loading animation in popover while fetching data from the server
         * It will auto over write the previous content of popover
         * If response is received from the server then that will overwrite the loading animation
        */
        this.#updatePopoverContentAndTitle({
            status: null,
            content: `
            <div class="d-flex justify-content-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>`
        })

        const request = new XMLHttpRequest();
        if (window.location.hostname == '127.0.0.1')
            request.open('GET', `http://127.0.0.1:5000/api/fetch-file-metadata/${this.fileId}`, async = true);
        else
            request.open('GET', `https://rdsbca.pythonanywhere.com/api/fetch-file-metadata/${this.fileId}`, async = true);

        request.send();
        request.onload = () => {
            let response = {};

            if (request.status == 200) {
                response = {
                    status: 200,
                    content: JSON.parse(request.responseText)
                };
            }
            else if (request.status == 400) {
                response = {
                    status: 400,
                    content: "Invalid Request"
                }
            }
            else if (request.status == 404) {
                response = {
                    status: 404,
                    content: `Not Found`
                };
            }
            else if (request.status >= 500) {
                response = {
                    status: request.status,
                    content: "Server Side Error. Client request ID 501"
                };
            }
            else {
                response = {
                    status: request.status,
                    content: "Unknown Error Occurred. Client request ID 502"
                };
            }
            this.#updatePopoverContentAndTitle(response);
        }
    }

    #updatePopoverContentAndTitle(response) {
        console.log("Called Update PopoverContent & Title")
        const popover = bootstrap.Popover.getOrCreateInstance(`button.info-button[file-id="${this.fileId}"]`) // Returns a Bootstrap popover instance
        if (response.status == 200) {
            /* setContent example
             * How to change/update/set title and content of popovers.
             * Source: https://getbootstrap.com/docs/5.2/components/popovers/
             */
            popover.setContent({
                '.popover-header': response.content.Title,
                '.popover-body': `  &bull; <b>Credit</b>: <a href="${!response.content.SubmitterContact ? 'javascript:void(0)' : response.content.SubmitterContact}" target="_blank">${response.content.SubmitterName}</a> ${response.content.SubmitterDesignation ? `<i>(${response.content.SubmitterDesignation})</i>` : ''}<br/>
                                    &bull; <b>Approver</b>: <a href="${!response.content.ApproverContact ? 'javascript:void(0)' : response.content.ApproverContact}" target="_blank">${response.content.ApproverName}</a> ${response.content.ApproverDesignation ? `<i>(${response.content.ApproverDesignation})</i>` : ''}<br/>                
                                    &bull; <b>Size</b>: ${response.content.Size} MB <br/>
                                    &bull; <b>Downloads</b>: ${!response.content.DownloadCount ? 0 : response.content.DownloadCount}<br/>
                                    ${window.screen.width <= 768 ? `&bull; <b> Views</b>: ${!response.content.ViewsCount ? 0 : response.content.ViewsCount}<br/>` : ''}
                                    &bull; <b>Last Downloaded</b>: ${!response.content.LastDownloaded ? 'N/A' : response.content.LastDownloaded} <br/>
                                    &bull; <b>Last Modified</b>: ${response.content.DateModified}</br>
                                    &bull; <b>Uploaded On</b>: ${response.content.UploadedOn}
                                `
            })
            /*In JavaScript, null and undefined are both considered falsy values, which means they evaluate to false in boolean expressions.*/
        }
        else {
            popover.setContent({
                '.popover-header': `File ID - ${this.fileId}`,
                '.popover-body': response.content
            })
        }
    }

    /*Method to display the metadata of the specified fileId.*/
    displayFileMetadata = () => {
        this.#fetchAndUpdateFileMetadata();
        console.log('called display file metadata');
    }
}

/*******Javascript to handle View button to view the file in new tab********/
/*Method to initialize view button by adding event listeners etc*/
function initializeViewButtons() {
    const viewButtons = document.querySelectorAll("td.phone-only > button")
    for (let object of viewButtons) {
        object.addEventListener('click', () => {
            viewTheFile(object);
        })
    }
}


/* function to view the file in new tab*/
const viewTheFile = (viewButton) => {
    const fileId = viewButton.getAttribute('file-id');
    console.log(fileId)

    if (!fileId) {
        console.log('File ID is not available');
        return;
    }
    const promise = new Promise((resolve, reject) => {
        const request = new XMLHttpRequest();
        if (window.location.hostname == '127.0.0.1')
            request.open('GET', `http://127.0.0.1:5000/api/fetch-file-view-link/${fileId}`, async = true);
        else
            request.open('GET', `https://rdsbca.pythonanywhere.com/api/fetch-file-view-link/${fileId}`, async = true);

        request.send();
        /*display loading animation in view button while fetching the view link from the server*/
        displayLoadingSpinner(viewButton);
        request.onload = () => {
            if (request.status == 200)
                resolve(request.responseText);
            else
                reject(request.status);
        }
    })

    promise.then((responseText) => {
        responseText = JSON.parse(responseText);
        console.log(responseText);
        /*removing the loading animation from view button*/
        viewButton.innerHTML = `<i class="material-icons icons">visibility</i>`
        window.open(responseText, target = "_blank");
    })
    promise.catch((status) => {
        console.log(`Error: ${status}`);
        /*removing the loading animation from view button*/
        viewButton.innerHTML = `<i class="material-icons icons">visibility</i>`
    });
}

displayLoadingSpinner = (element) => {
    element.innerHTML = `
                        <div class="spinner-border text-primary spinner-border-sm" role="status">
                        <span class="visually-hidden">Loading...</span>
                        </div>
                        `
}