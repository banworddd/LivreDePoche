document.addEventListener("DOMContentLoaded", function() {
    const bookId = window.location.pathname.split("/")[2];  // Извлекаем book_id из URL

    const addToReadingListButtons = document.querySelectorAll("#reading-list-buttons button");
    const username = document.getElementById('reading-list-buttons')?.dataset.username;
    const reviewsList = document.getElementById('reviews-list');
    const userReviewHeader = document.getElementById('user-review-header');

    // Функция для получения информации о книге через API
    function fetchBookDetails() {
        fetch(`/api/book/${bookId}/`)
            .then(response => response.json())
            .then(data => {
                // Обновляем данные на странице
                document.getElementById('book-title').textContent = data.title;
                document.getElementById('book-author').textContent = data.author;
                document.getElementById('book-description').textContent = data.description;
                document.getElementById('book-year').textContent = data.year;
            })
            .catch(error => {
                console.error("Ошибка при загрузке данных о книге:", error);
            });
    }

    // Функция для получения отзывов через API
    function fetchReviews() {
        fetch(`/api/book/${bookId}/reviews/`)
            .then(response => response.json())
            .then(data => {
                reviewsList.innerHTML = "";  // Очищаем список отзывов

                let userReviewFound = false;

                // Проверяем, есть ли отзыв у текущего пользователя
                const userReview = data.find(review => review.user === username);

                // Если отзыв пользователя есть, выводим его в хедер
                if (userReview) {
                    userReviewFound = true;
                    userReviewHeader.innerHTML = `
                        <div class="user-review">
                            <strong>${userReview.user}</strong> - ${userReview.rating}⭐
                            <p>${userReview.review_text}</p>
                            <small>Дата: ${new Date(userReview.review_date).toLocaleDateString()}</small>
                            <button class="edit-review" data-id="${userReview.id}">Редактировать</button>
                            <button class="delete-review" data-id="${userReview.id}">Удалить</button>
                        </div>
                    `;
                }

                // Если у пользователя нет отзыва, показываем форму
                if (!userReviewFound) {
                    userReviewHeader.innerHTML = `
                        <h3>Добавить отзыв</h3>
                        <form id="review-form">
                            <label for="rating">Оценка:</label>
                            <select id="rating" name="rating" required>
                                <option value="1">1</option>
                                <option value="2">2</option>
                                <option value="3">3</option>
                                <option value="4">4</option>
                                <option value="5">5</option>
                            </select>
                            <br>
                            <label for="review-text">Текст отзыва:</label>
                            <textarea id="review-text" name="review_text" rows="4" required></textarea>
                            <br>
                            <button type="submit">Добавить отзыв</button>
                        </form>
                    `;
                }

                // Отображаем остальные отзывы
                data.forEach(review => {
                    if (review.user !== username) {
                        const reviewItem = document.createElement('li');
                        reviewItem.innerHTML = `
                            <strong>${review.user}</strong> - ${review.rating}⭐
                            <p>${review.review_text}</p>
                            <small>Дата: ${new Date(review.review_date).toLocaleDateString()}</small>
                        `;
                        reviewsList.appendChild(reviewItem);
                    }
                });

                // Привязываем обработчик события submit к форме после её добавления
                const reviewForm = document.getElementById('review-form');
                if (reviewForm) {
                    reviewForm.addEventListener("submit", submitReview);
                }

                // Привязываем обработчики событий для кнопок "Редактировать" и "Удалить"
                const editButtons = document.querySelectorAll('.edit-review');
                editButtons.forEach(button => {
                    button.addEventListener('click', () => {
                        const reviewId = button.getAttribute('data-id');
                        editReview(reviewId);
                    });
                });

                const deleteButtons = document.querySelectorAll('.delete-review');
                deleteButtons.forEach(button => {
                    button.addEventListener('click', () => {
                        const reviewId = button.getAttribute('data-id');
                        deleteReview(reviewId);
                    });
                });
            })
            .catch(error => {
                console.error("Ошибка при загрузке отзывов:", error);
            });
    }

    // Функция для отправки нового отзыва
    function submitReview(event) {
        event.preventDefault();
        const rating = document.getElementById('rating').value;
        const reviewText = document.getElementById('review-text').value;

        const reviewData = {
            rating: rating,
            review_text: reviewText
        };

        fetch(`/api/book/${bookId}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(reviewData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                fetchReviews(); // Обновить список отзывов после успешного добавления
                window.location.href = `/book/${bookId}/`;  // Перенаправить обратно на страницу книги
            } else {
                console.error('Ошибка при добавлении отзыва:', data);
            }
        })
        .catch(error => {
            console.error("Ошибка при отправке отзыва:", error);
        });
    }

    // Функция для редактирования отзыва
    function editReview(reviewId) {
        const reviewElement = document.querySelector(`[data-id="${reviewId}"]`).parentElement;
        const reviewText = reviewElement.querySelector('p').textContent;
        const rating = reviewElement.querySelector('strong').textContent[0];  // Получаем рейтинг

        // Заполняем форму редактирования
        userReviewHeader.innerHTML = `
            <h3>Редактировать отзыв</h3>
            <form id="review-form" data-review-id="${reviewId}">
                <label for="rating">Оценка:</label>
                <select id="rating" name="rating" required>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                </select>
                <br>
                <label for="review-text">Текст отзыва:</label>
                <textarea id="review-text" name="review_text" rows="4" required>${reviewText}</textarea>
                <br>
                <button type="submit">Обновить отзыв</button>
            </form>
        `;

        // Устанавливаем значение рейтинга
        document.getElementById('rating').value = rating;

        // Привязываем обработчик события submit к форме после её добавления
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.addEventListener("submit", updateReview);
        }
    }

    // Функция для обновления отзыва
    function updateReview(event) {
        event.preventDefault();
        const reviewId = event.target.getAttribute('data-review-id');
        const rating = document.getElementById('rating').value;
        const reviewText = document.getElementById('review-text').value;

        const reviewData = {
            rating: rating,
            review_text: reviewText
        };

        fetch(`/api/book/${bookId}/reviews/${reviewId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(reviewData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                fetchReviews(); // Обновить список отзывов после успешного обновления
                window.location.href = `/book/${bookId}/`;  // Перенаправить обратно на страницу книги
            } else {
                console.error('Ошибка при обновлении отзыва:', data);
            }
        })
        .catch(error => {
            console.error("Ошибка при обновлении отзыва:", error);
        });
    }

    // Функция для удаления отзыва
    function deleteReview(reviewId) {
        if (window.confirm("Вы уверены, что хотите удалить этот отзыв?")) {
            fetch(`/api/book/${bookId}/reviews/${reviewId}/`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
            }).then(() => fetchReviews());
        }
    }

    // Функция для добавления книги в список
    function addToReadingList(event) {
        const status = event.target.getAttribute('data-status');

        const url = `/api/reading_list/${username}/`;

        const data = {
            book: bookId,
            status: status
        };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .catch(error => {
            console.error('Ошибка:', error);
        });
    }

    // Загрузка данных о книге и отзывах при загрузке страницы
    fetchBookDetails();
    fetchReviews();

    addToReadingListButtons.forEach(button => {
        button.addEventListener("click", addToReadingList);
    });
});

// Функция для получения CSRF токена из cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            const [key, value] = cookie.trim().split('=');
            if (key === name) {
                cookieValue = value;
            }
        });
    }
    return cookieValue;
}
