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
    })
    // document.getElementById('submit-button').addEventListener('click', displayPreviousYearQuestions);
})