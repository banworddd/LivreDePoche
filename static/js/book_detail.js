document.addEventListener("DOMContentLoaded", function() {
    const bookId = window.location.pathname.split("/")[2];  // Извлекаем book_id из URL
    const reviewsList = document.getElementById('reviews-list');
    const reviewForm = document.getElementById('review-form');
    const addToReadingListButtons = document.querySelectorAll("#reading-list-buttons button");
    const username = document.getElementById('reading-list-buttons')?.dataset.username;
    const reviewFormContainer = document.getElementById('review-form-container');

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

                if (userReview) {
                    userReviewFound = true;
                    // Выводим отзыв пользователя
                    const userReviewItem = document.createElement('li');
                    userReviewItem.classList.add('user-review');  // Класс для выделения отзыва пользователя
                    userReviewItem.innerHTML = `
                        <strong>${userReview.user}</strong> - ${userReview.rating}⭐
                        <p>${userReview.review_text}</p>
                        <small>Дата: ${new Date(userReview.review_date).toLocaleDateString()}</small>
                        <button class="edit-review" data-id="${userReview.id}">Редактировать</button>
                        <button class="delete-review" data-id="${userReview.id}">Удалить</button>
                    `;
                    reviewsList.appendChild(userReviewItem);
                }

                // Если у пользователя нет отзыва, показываем форму
                if (!userReviewFound) {
                    reviewFormContainer.style.display = 'block';  // Показываем форму для отзыва
                } else {
                    reviewFormContainer.style.display = 'none';  // Скрываем форму, если отзыв уже есть
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
                fetchReviews(); // Обновить список отзывов
                reviewForm.reset(); // Очистить форму
            } else {
                console.error('Ошибка при добавлении отзыва:', data);
            }
        });
    }

    // Функция для редактирования отзыва
    function editReview(reviewId) {
        const reviewText = document.querySelector(`[data-id="${reviewId}"]`).previousElementSibling.textContent;
        const rating = document.querySelector(`[data-id="${reviewId}"]`).previousElementSibling.previousElementSibling.textContent[0];  // Получаем рейтинг

        // Заполняем форму редактирования
        document.getElementById('review-text').value = reviewText;
        document.getElementById('rating').value = rating;

        // Отображаем форму редактирования
        reviewFormContainer.style.display = 'block';

        // Убираем отзыв пользователя
        const userReviewItem = document.querySelector(`[data-id="${reviewId}"]`).parentElement;
        userReviewItem.remove();
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

    // Обработчики событий
    reviewForm.addEventListener('submit', submitReview);
    reviewsList.addEventListener('click', function(event) {
        if (event.target.classList.contains('edit-review')) {
            const reviewId = event.target.getAttribute('data-id');
            editReview(reviewId);
        }
        if (event.target.classList.contains('delete-review')) {
            const reviewId = event.target.getAttribute('data-id');
            deleteReview(reviewId);
        }
    });

    addToReadingListButtons.forEach(button => {
        button.addEventListener("click", addToReadingList);
    });
});

// Функция для получения CSRF токена из cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
