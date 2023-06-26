
/*fetch form from the server and display */
const dropDown = document.getElementById("floatingSelect2");
dropDown.addEventListener('change', () => {
    if (dropDown.value != "") {
        fetchFormAndDisplay(selectedOption = dropDown.value);
    }
    else {
        document.getElementById("response-text-container").innerHTML = `
                                                    <div class="alert alert-danger" role="alert">
                                                        Please select an option from the above dropdown
                                                    </div>
                                                    `;
    }
})

const fetchFormAndDisplay = function (selectedOption) {

    /*displaying loading animation/spinner while making the request and receiving the response from the server*/
    const responseTextContainer = document.getElementById("response-text-container");
    responseTextContainer.innerHTML = `
                                        <div class="spinner-border text-primary" role="status">
                                            <span class="visually-hidden">Loading...</span>
                                        </div>
                                        `;

    const promise = new Promise((resolve, reject) => {
        const request = new XMLHttpRequest();
        if (window.location.hostname == '127.0.0.1')
            request.open('POST', url = 'http://127.0.0.1:5000/api/fetch-contribution-form', true);
        else
            request.open('POST', url = 'https://rdsbca.pythonanywhere.com/api/fetch-contribution-form', true);

        request.setRequestHeader('Content-Type', 'application/json')
        request.send(JSON.stringify({ selectedOption: selectedOption }));
        request.onload = () => {
            if (request.status == 200)
                resolve(request.responseText);
            else
                reject(request.responseText);
        }
    });

    promise.then((responseText) => {
        responseTextContainer.innerHTML = responseText;
        /*Executing the script related to selection contribution page fetched from the server successfully*/
        executeScriptOfCurrentContributionPage(page = dropDown.value);
    })

    promise.catch((error) => {
        responseTextContainer.innerHTML = responseText;
    })

}

/**
 * @param {currently available contribution page} page 
 * Function to execute the script related to the currently available contribution page fetched from the server.
 */
const executeScriptOfCurrentContributionPage = (page) => {
    if (page == 'previous-year-questions')
        contributePreviousYearQuestionScript();
}

/***********************************************************
  * @script_related_to_contribution_of_previous_year_questions
  * @starts
  */

const contributePreviousYearQuestionScript = () => {
    /*functionality to select file if user clicks on the div containing the file input type*/
    document.getElementById('file-div').addEventListener('click', () => {
        document.getElementById('file').click();
    });

    /* When user clicks on the input type file then explorer opens twice due to above event listener on the 'file-div'
     * So, to fix this we have to use event.stopPropagation() method which prevents event from reaching any objects other than the current object.
     * So, due to this event will not propagate/reach to the file-div and that event listener will not listen the event and everything will work as expected.
    */
    document.getElementById('file').addEventListener('click', (event) => {
        event.stopPropagation();
    })

    /*functionality to display the hidden input type to write the source name if user selects 'others' in the source dropdown*/
    const sourceDropdown = document.querySelector('select[name=source]');
    sourceDropdown.addEventListener('change', () => {
        const otherSourceDiv = document.getElementById('other-source');
        if (sourceDropdown.value == 'others') {
            otherSourceDiv.style.display = '';
        }
        else {
            otherSourceDiv.style.display = 'none';
        }
    })
}

/**
 * @script_related_to_contribution_of_previous_year_questions
 * @ends
 **************************************************************/