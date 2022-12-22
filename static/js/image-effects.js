const images = document.querySelectorAll('.images');
/*adding event listener to each image*/
images.forEach(image => image.addEventListener('click', () => {
    image.style.animation = 'rotate 0.5s linear';
    setTimeout(() => {
        image.style.removeProperty('animation');
        /*we can also use image.style.animation = '';*/
    }, 1000);
}))