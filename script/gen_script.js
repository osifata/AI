document.addEventListener('DOMContentLoaded', () => {
    const leftBtn = document.querySelector('#arrow-left');
    const rightBtn = document.querySelector('#arrow-right');
    const imageWrapper = document.querySelector('.image-wrapper');
    const images = document.querySelectorAll('.slide');
    const continueBtn = document.querySelector('.continue-btn');
    let currentIndex = 0;

    function updateScroll() {
        const offset = currentIndex * (100 / 3); // Adjust offset based on image width
        imageWrapper.style.transform = `translateX(-${offset}%)`;
    }

    leftBtn.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            updateScroll();
        }
    });

    rightBtn.addEventListener('click', () => {
        if (currentIndex < images.length - 3) { // Allow scrolling till the last set of images
            currentIndex++;
            updateScroll();
        }
    });

    images.forEach(image => {
        image.addEventListener('click', () => {
            images.forEach(img => img.classList.remove('selected'));
            image.classList.add('selected');
            continueBtn.style.display = 'block';
        });
    });
});
