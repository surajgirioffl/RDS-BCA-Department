function overlay() {
    if (sessionStorage.getItem('isOverlayClosed') === 'True') return;
    const element = document.getElementById('overlay');
    setTimeout(() => { _overlay(element) }, 2000)
}

var called = 0;
function _overlay(element) {
    element.style.display = "block";
    document.body.addEventListener('keydown', (event) => {
        event.key === 'Escape' ? closeOverlay(element) : null;
    });
    closeAfter();

    function closeAfter() {
        let timeout = setTimeout(closeAfter, 1000);/*call again in 1 sec*/
        document.getElementById('autoClose').innerHTML = `Auto close in ${10 - called} seconds`;
        called++;
        console.log(called);
        if (called == 11) {
            clearTimeout(timeout);
            closeOverlay(element);
        }
    }
}

function closeOverlay(element) {
    if (element === undefined)
        element = document.getElementById('overlay');
    element.style.animation = "slideUpFromCenter 1s ease-in-out";
    setTimeout(() => {
        element.style.display = 'none';
    }, 1000);
    sessionStorage.setItem('isOverlayClosed', 'True');
}