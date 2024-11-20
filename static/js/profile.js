document.addEventListener("DOMContentLoaded", function() {
    const profileContainer = document.querySelector('.profile-container');
    const username = profileContainer.dataset.username;  // Извлекаем имя пользователя
    const csrfToken = profileContainer.dataset.csrf;

    // Показ карандаша на аватарке
    const avatarImage = document.getElementById('avatar-image');
    const avatarOverlay = document.querySelector('.avatar-overlay');
    const avatarInput = document.getElementById('avatar');

    avatarImage?.addEventListener('mouseenter', () => {
        avatarOverlay.style.display = 'flex';
    });

    avatarOverlay?.addEventListener('mouseleave', () => {
        avatarOverlay.style.display = 'none';
    });

    // Показ формы изменения аватара при клике на карандаш
    avatarOverlay?.addEventListener('click', () => {
        avatarInput.click();  // Открываем диалог выбора файла
    });

    // Обработчик для загрузки аватара
    avatarInput?.addEventListener('change', function() {
        const file = avatarInput.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('avatar', file);

            // Отправляем файл на сервер
            fetch(`/api/profile/${username}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                }
            })
            .then(response => {
                if (response.ok) {
                    // Обновляем изображение аватара
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        avatarImage.src = e.target.result;  // Обновляем аватар
                        avatarImage.style.display = 'block';  // Показываем изображение
                    };
                    reader.readAsDataURL(file);  // Показываем аватар до загрузки на сервер
                } else {
                    console.error('Ошибка при обновлении аватара.');
                }
            })
            .catch(error => console.error('Ошибка при отправке запроса на обновление аватара:', error));
        }
    });

    // Сохранение биографии по нажатию Enter
    document.getElementById('bio')?.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {  // Если нажата клавиша Enter без Shift
            event.preventDefault();  // Предотвращаем новую строку

            const newBio = this.value.trim();

            // Отправляем обновлённую биографию на сервер через FormData
            const formData = new FormData();
            formData.append('bio', newBio);

            fetch(`/api/profile/${username}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,  // CSRF токен для безопасности
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json();  // Ожидаем JSON-ответ
                } else {
                    throw new Error('Ошибка при сохранении биографии');
                }
            })
            .then(data => {
                // Перезагружаем страницу после успешного сохранения
                location.reload();
            })
            .catch(error => {
                console.error('Ошибка при отправке запроса на сохранение биографии:', error);
            });
        }
    });

    // Загружаем информацию о пользователе
    fetch(`/api/profile/${username}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('user-email').innerText = data.email || "Нет информации";
            document.getElementById('user-bio').innerText = data.bio || "Нет информации";

            if (data.avatar) {
                const avatarImage = document.getElementById('avatar-image');
                avatarImage.src = data.avatar;
                avatarImage.style.display = 'block';
            }
        })
        .catch(error => console.error('Ошибка при загрузке информации о пользователе:', error));

    // Код для отображения формы редактирования биографии
    if (document.getElementById('edit-bio')) {
        document.getElementById('edit-bio').addEventListener('click', () => {
            const bioText = document.getElementById('user-bio');
            const bioForm = document.getElementById('bio-form');
            const bioTextarea = document.getElementById('bio');

            bioTextarea.value = bioText.innerText.trim();
            bioText.style.display = 'none';
            bioForm.style.display = 'block';
        });
    }

        // Загрузка списка чтения
        fetch(`/api/reading_list/${username}/`)
            .then(response => response.json())
            .then(data => {
                const currentlyReadingList = document.getElementById('currently-reading-list');
                const completedList = document.getElementById('completed-list');
                const toReadList = document.getElementById('to-read-list');

                currentlyReadingList.innerHTML = '';
                completedList.innerHTML = '';
                toReadList.innerHTML = '';

                if (data.length === 0) {
                    currentlyReadingList.innerHTML = '<li>Нет книг в списке чтения.</li>';
                    completedList.innerHTML = '<li>Нет завершенных книг.</li>';
                    toReadList.innerHTML = '<li>Нет книг, которые планируете прочитать.</li>';
                } else {
                    const bookRequests = data.map(item => {
                        return fetch(`/api/book/${item.book}/`);
                    });

                    Promise.all(bookRequests)
                        .then(responses => Promise.all(responses.map(res => res.json())))
                        .then(books => {
                            books.forEach((book, index) => {
                                const item = data[index];
                                const li = document.createElement('li');
                                li.classList.add('book-card');
                                li.innerHTML = `
                                    <a href="/book/${book.id}/">${book.title}</a>
                                    ${item.read_date ? ` - Прочитано: ${item.read_date}` : ''}
                                `;

                                // Если это владелец, показываем кнопку удаления
                                if ("{{ is_owner }}" === "True") {
                                    const deleteButton = document.createElement('button');
                                    deleteButton.classList.add('delete-button');
                                    deleteButton.innerHTML = '×';
                                    deleteButton.onclick = function() {
                                        deleteBook(item.id); // Вызов функции удаления
                                    };
                                    li.appendChild(deleteButton);
                                }

                                // Добавляем книгу в соответствующий список
                                if (item.status === 'currently_reading') {
                                    currentlyReadingList.appendChild(li);
                                } else if (item.status === 'completed') {
                                    completedList.appendChild(li);
                                } else if (item.status === 'planned') {
                                    toReadList.appendChild(li);
                                }
                            });
                        })
                        .catch(error => console.error('Ошибка при загрузке информации о книгах:', error));
                }
            })
            .catch(error => console.error('Ошибка при загрузке списка чтения:', error));

        // Функция удаления книги
        function deleteBook(readingListId) {
            fetch(`/api/reading_list/${username}/${readingListId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(() => location.reload())
            .catch(error => console.error('Ошибка при удалении книги:', error));
        }


    // Загрузка отзывов
    const reviewsList = document.getElementById('reviews-list');
    const loadingItem = reviewsList.querySelector('.review-item'); // Элемент "Загрузка..."

    // Показать загрузку, пока данные не загружены
    loadingItem.innerHTML = 'Загрузка...';

    fetch(`/api/user_reviews/${username}/`)  // Используем переменную username для URL
        .then(response => response.json())
        .then(data => {
            reviewsList.innerHTML = ''; // Очищаем список

            if (data.length === 0) {
                reviewsList.innerHTML = '<li class="review-item list-group-item" style="box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); background-color: #f9f9f9; border-radius: 10px; padding: 15px; margin-bottom: 15px;">Нет отзывов.</li>';
            } else {
                data.forEach(review => {
                    const li = document.createElement('li');
                    li.classList.add('review-item', 'list-group-item');
                    li.innerHTML = `
                        <strong><a href="/book/${review.book_id}/">${review.book_title}</a></strong> <br>
                        Рейтинг: ${getRatingStars(review.rating)}<br>
                        <strong>Отзыв:</strong> ${review.review_text}<br>
                        <small>Дата отзыва: ${review.review_date}</small>
                    `;
                    function getRatingStars(rating) {
                        let stars = '';
                        for (let i = 1; i <= 5; i++) {
                            if (i <= rating) {
                                stars += '★'; // Заполненная звезда
                            } else {
                                stars += '☆'; // Пустая звезда
                            }
                        }
                        return stars;
}
                    reviewsList.appendChild(li);
                });
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке отзывов:', error);
            reviewsList.innerHTML = '<li class="review-item list-group-item" style="box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); background-color: #f9f9f9; border-radius: 10px; padding: 15px; margin-bottom: 15px;">Не удалось загрузить отзывы.</li>';
        });
});
