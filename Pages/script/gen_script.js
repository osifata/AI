document.addEventListener('DOMContentLoaded', () => {
    const leftBtn = document.querySelector('#arrow-left');
    const rightBtn = document.querySelector('#arrow-right');
    const imageWrapper = document.querySelector('.image-wrapper');
    const images = document.querySelectorAll('.slide');
    const continueBtn = document.querySelector('.continue-btn');
    let currentIndex = 0; // Изменяем начальный индекс на второе изображение

    function updateScroll() {
        const offset = currentIndex * -95; // Рассчитываем смещение
        imageWrapper.style.transform = `translateX(${offset}%)`;
    }

    leftBtn.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            updateScroll();
        }
    });

    rightBtn.addEventListener('click', () => {
        if (currentIndex < images.length - 1) { // Добавляем проверку для правой кнопки
            currentIndex++;
            updateScroll();
        }
    });

    // Дополнительно: обработчик кликов на изображениях для выделения выбранного
    images.forEach((image, index) => {
        image.addEventListener('click', () => {
            currentIndex = index; // Устанавливаем текущий индекс при клике на изображение
            updateScroll();
            images.forEach(img => img.classList.remove('selected'));
            image.classList.add('selected');
            continueBtn.style.display = 'block';
        });
    });
});
