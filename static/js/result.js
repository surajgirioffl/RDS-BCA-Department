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