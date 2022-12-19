function reset() {
    const inputElements = document.getElementsByTagName('input');
    for (let i = 0; i < inputElements.length; i++) {
        inputElements[i].value = '';
    }
}