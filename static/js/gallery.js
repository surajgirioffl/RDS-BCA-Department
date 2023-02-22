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
}

(() => {
    const images = document.querySelectorAll('.image');
    images.forEach(image => {
        image.addEventListener('click', () => {
            displayFullScreen(image);
        })
    })
})()