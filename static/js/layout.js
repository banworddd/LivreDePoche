        document.addEventListener('DOMContentLoaded', () => {
            const userMenu = document.querySelector('.user-menu');
            if (userMenu) {
                userMenu.addEventListener('click', (e) => {
                    e.stopPropagation();
                    userMenu.classList.toggle('active');
                });

                // Закрытие меню при клике вне
                document.addEventListener('click', () => {
                    userMenu.classList.remove('active');
                });
            }
        });
document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.site-header');
    let lastScrollTop = 0; // Переменная для отслеживания последней позиции скролла
    let isHeaderHidden = false; // Флаг для отслеживания состояния хедера (скрыт/показан)

    // При прокрутке скрываем или показываем хедер
    window.addEventListener('scroll', () => {
        let scrollTop = window.scrollY || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop) {
            // Прокручено вниз, скрыть хедер
            if (!isHeaderHidden) {
                header.classList.add('hidden');
                isHeaderHidden = true;
            }
        } else {
            // Прокручено вверх, показать хедер
            if (isHeaderHidden) {
                header.classList.remove('hidden');
                isHeaderHidden = false;
            }
        }
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // Для предотвращения прокрутки вверх на 0
    });

    // Показать хедер при наведении на верхнюю границу страницы (только если скрыт)
    header.addEventListener('mouseenter', () => {
        if (isHeaderHidden) { // Показываем хедер только если он скрыт
            header.classList.remove('hidden');
            isHeaderHidden = false;
        }
    });

    // Скрыть хедер, если курсор уходит с верхней границы страницы
    header.addEventListener('mouseleave', () => {
        if (window.scrollY > 0 && !isHeaderHidden) { // Если страница прокручена вниз и хедер не скрыт
            header.classList.add('hidden');
            isHeaderHidden = true;
        }
    });

    // Обработка события, чтобы хедер появился при наведении на верхнюю границу, если он скрыт
    document.body.addEventListener('mousemove', (event) => {
        // Если страница прокручена вниз и курсор находится в верхней области
        if (window.scrollY > 0 && isHeaderHidden && event.clientY < 50) {
            header.classList.remove('hidden');
            isHeaderHidden = false;
        }
    });
});
