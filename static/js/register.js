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