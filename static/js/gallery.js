/**
 * @param {object} image: image element to be displayed in full screen.
 */
function displayFullScreen(image) {
    const fullScreenContainer = document.createElement('div');
    fullScreenContainer.id = 'fullscreen-div';

    /*button to view previous image */
    const previousImageButton = document.createElement('span');
    previousImageButton.className = "carousel-control-prev-icon";
    previousImageButton.addEventListener('click', () => {
        if (image.previousElementSibling.src != null) {
            image = image.previousElementSibling;
            copyImage.src = image.src;
        }
    })
    fullScreenContainer.appendChild(previousImageButton);

    /*div containing images*/
    const imageContainer = document.createElement('div');
    imageContainer.id = 'image-container-div';
    fullScreenContainer.appendChild(imageContainer);

    /*image which is displaying currently*/
    let copyImage = document.createElement('img');
    copyImage.src = image.src;
    imageContainer.appendChild(copyImage);
    console.log('done');

    /*button to view next image */
    const nextImageButton = document.createElement('span');
    nextImageButton.className = "carousel-control-next-icon";
    nextImageButton.addEventListener('click', () => {
        if (image.nextElementSibling.src != null) {
            image = image.nextElementSibling;
            copyImage.src = image.src;
        }
    })
    fullScreenContainer.appendChild(nextImageButton);

    /*appending the main fullScreenContainer to the body*/
    document.body.appendChild(fullScreenContainer);

    /**
     * @special keyboard shortcuts to navigate through images, to exit full screen, to visit home page and more...
     * some event listeners for ease of use with the help of keyboard.
     */
    document.body.addEventListener('keydown', (event) => {
        /*removing the full screen container on pressing escape*/
        if (event.key == 'Escape') {
            fullScreenContainer.remove();
        }
        /*viewing next image on pressing right arrow key*/
        else if (event.key == 'ArrowRight') {
            if (image.nextElementSibling.src != null) {
                image = image.nextElementSibling;
                copyImage.src = image.src;
            }
        }
        /*viewing previous image on pressing left arrow key*/
        else if (event.key == 'ArrowLeft') {
            if (image.previousElementSibling.src != null) {
                image = image.previousElementSibling;
                copyImage.src = image.src;
            }
        }
        else if (event.key === 'h' || event.key === 'H') {
            document.querySelectorAll('div> ul> li')[0].firstElementChild.click();
            console.log('clicked')
        }
        console.log(event)
    })
}

(() => {
    const images = document.querySelectorAll('.image');
    images.forEach(image => {
        image.addEventListener('click', () => {
            displayFullScreen(image);
        })
    })
})()