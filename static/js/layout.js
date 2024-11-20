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