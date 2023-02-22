/**
 * @param {object} image: image element to be displayed in full screen.
 */
function displayFullScreen(image) {
    const fullScreenContainer = document.createElement('div');
    fullScreenContainer.id = 'fullscreen-div';

    /*div containing images*/
    const imageContainer = document.createElement('div');
    imageContainer.id = 'image-container-div';
    fullScreenContainer.appendChild(imageContainer);

    /*image which is displaying currently*/
    let copyImage = document.createElement('img');
    copyImage.src = image.src;
    imageContainer.appendChild(copyImage);
    console.log('done');

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