document.addEventListener("DOMContentLoaded", function() {
    const bookId = window.location.pathname.split("/")[2];
    const addToReadingListButtons = document.querySelectorAll("#reading-list-buttons button");
    const username = document.getElementById('reading-list-buttons')?.dataset.username;
    const reviewsList = document.getElementById('reviews-list');
    const userReviewHeader = document.getElementById('user-review-header');
    let selectedRating = 0;

    function fetchBookDetails() {
        fetch(`/api/book/${bookId}/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('book-title').textContent = data.title;
                document.getElementById('book-author').textContent = data.authors.length > 0 ? data.authors[0].name : 'Неизвестный автор';
                document.getElementById('book-description').textContent = data.description;
            })
            .catch(error => {
                console.error("Ошибка при загрузке данных о книге:", error);
            });
    }

    function fetchReviews() {
        fetch(`/api/book/${bookId}/reviews/`)
            .then(response => response.json())
            .then(data => {
                reviewsList.innerHTML = "";
                let userReviewFound = false;
                const userReview = data.find(review => review.user === username);

                if (userReview) {
                    userReviewFound = true;
                    userReviewHeader.innerHTML = `
                        <div class="user-review">
                            <strong>${userReview.user}</strong> - ${userReview.rating}⭐
                            <p>${userReview.review_text}</p>
                            <small>Дата: ${new Date(userReview.review_date).toLocaleDateString()}</small>
                            <button class="edit-review btn" data-id="${userReview.id}">Редактировать</button>
                            <button class="delete-review btn" data-id="${userReview.id}">Удалить</button>
                        </div>
                    `;
                }

                if (!userReviewFound) {
                    userReviewHeader.innerHTML = `
                        <h3>Добавить отзыв</h3>
                        <div id="rating-stars" class="rating-stars">
                            <span class="star" data-value="1">☆</span>
                            <span class="star" data-value="2">☆</span>
                            <span class="star" data-value="3">☆</span>
                            <span class="star" data-value="4">☆</span>
                            <span class="star" data-value="5">☆</span>
                        </div>
                        <form id="review-form">
                            <textarea id="review-text" name="review_text" rows="4" class="review-textarea" required></textarea>
                            <div id="rating-error" class="error-message" style="display: none;">Пожалуйста, выберите рейтинг перед отправкой отзыва.</div>
                            <br>
                            <button type="submit" class="btn">Добавить отзыв</button>
                        </form>
                    `;
                }

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

                const reviewForm = document.getElementById('review-form');
                if (reviewForm) {
                    reviewForm.addEventListener("submit", submitReview);
                }

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

                const stars = document.querySelectorAll('.star');
                stars.forEach(star => {
                    star.addEventListener('click', () => {
                        selectedRating = star.getAttribute('data-value');
                        updateStars(selectedRating);
                        document.getElementById('rating-error').style.display = 'none'; // Скрываем сообщение об ошибке при выборе рейтинга
                    });
                });
            })
            .catch(error => {
                console.error("Ошибка при загрузке отзывов:", error);
            });
    }

    function submitReview(event) {
        event.preventDefault();
        const ratingError = document.getElementById('rating-error');
        if (selectedRating === 0) {
            ratingError.style.display = 'block';
            return;
        }
        const reviewText = document.getElementById('review-text').value;

        const reviewData = {
            rating: selectedRating,
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
                fetchReviews();
                window.location.href = `/book/${bookId}/`;
            } else {
                console.error('Ошибка при добавлении отзыва:', data);
            }
        })
        .catch(error => {
            console.error("Ошибка при отправке отзыва:", error);
        });
    }

    function editReview(reviewId) {
        const reviewElement = document.querySelector(`[data-id="${reviewId}"]`).parentElement;
        const reviewText = reviewElement.querySelector('p').textContent;
        const rating = reviewElement.querySelector('strong').textContent[0];

        userReviewHeader.innerHTML = `
            <h3>Редактировать отзыв</h3>
            <div id="rating-stars" class="rating-stars">
                <span class="star" data-value="1">☆</span>
                <span class="star" data-value="2">☆</span>
                <span class="star" data-value="3">☆</span>
                <span class="star" data-value="4">☆</span>
                <span class="star" data-value="5">☆</span>
            </div>
            <form id="review-form" data-review-id="${reviewId}">
                <textarea id="review-text" name="review_text" rows="4" class="review-textarea" required>${reviewText}</textarea>
                <div id="rating-error" class="error-message" style="display: none;">Пожалуйста, выберите рейтинг перед отправкой отзыва.</div>
                <br>
                <button type="submit" class="btn">Обновить отзыв</button>
            </form>
        `;

        selectedRating = 0; // Сброс выбранного рейтинга
        updateStars(selectedRating);

        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.addEventListener("submit", updateReview);
        }

        const stars = document.querySelectorAll('.star');
        stars.forEach(star => {
            star.addEventListener('click', () => {
                selectedRating = star.getAttribute('data-value');
                updateStars(selectedRating);
                document.getElementById('rating-error').style.display = 'none'; // Скрываем сообщение об ошибке при выборе рейтинга
            });
        });
    }

    function updateReview(event) {
        event.preventDefault();
        const ratingError = document.getElementById('rating-error');
        if (selectedRating === 0) {
            ratingError.style.display = 'block';
            return;
        }
        const reviewId = event.target.getAttribute('data-review-id');
        const reviewText = document.getElementById('review-text').value;

        const reviewData = {
            rating: selectedRating,
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
                fetchReviews();
                window.location.href = `/book/${bookId}/`;
            } else {
                console.error('Ошибка при обновлении отзыва:', data);
            }
        })
        .catch(error => {
            console.error("Ошибка при обновлении отзыва:", error);
        });
    }

    function deleteReview(reviewId) {
        if (window.confirm("Вы уверены, что хотите удалить этот отзыв?")) {
            fetch(`/api/book/${bookId}/reviews/${reviewId}/`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
            }).then(() => fetchReviews());
        }
    }

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

    function updateStars(rating) {
        const stars = document.querySelectorAll('.star');
        stars.forEach(star => {
            star.classList.remove('selected');
            if (star.getAttribute('data-value') <= rating) {
                star.classList.add('selected');
                star.textContent = '★';
            } else {
                star.textContent = '☆';
            }
        });
    }

    fetchBookDetails();
    fetchReviews();

    addToReadingListButtons.forEach(button => {
        button.addEventListener("click", addToReadingList);
    });
});

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