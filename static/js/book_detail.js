document.addEventListener("DOMContentLoaded", function() {
    const bookId = window.location.pathname.split("/")[2];
    const addToReadingListButtons = document.querySelectorAll("#reading-list-buttons button");
    const username = document.getElementById('reading-list-buttons')?.dataset.username;
    const reviewsList = document.getElementById('reviews-list');
    const userReviewHeader = document.getElementById('user-review-header');
    let selectedRating = 0;

    function fetchBookDetails() {
        fetch(`/api/books/book/${bookId}/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('book-title').textContent = data.title;
                document.getElementById('book-author').textContent = data.authors.map(author => `${author.first_name} ${author.middle_name} ${author.last_name}`.trim()).join(", ");
                document.getElementById('book-description').textContent = data.description;

                // Формируем URL для запроса к API рейтинга книги
                const ratingApiUrl = `/api/users/rating_reviews/${bookId}/`;

                // Отправляем запрос к API рейтинга книги
                fetch(ratingApiUrl)
                    .then(response => response.json())
                    .then(ratingData => {
                        const ratingContainer = document.createElement('div');
                        ratingContainer.classList.add('rating');
                        if (ratingData.average_rating !== null) {
                            ratingContainer.innerHTML = `Средний рейтинг: ${ratingData.average_rating.toFixed(2)}`;
                        } else {
                            ratingContainer.innerHTML = 'Рейтинг еще не сформирован';
                        }
                        document.querySelector('.book-detail-container').appendChild(ratingContainer);
                    })
                    .catch(error => {
                        console.error(`Ошибка при загрузке рейтинга для книги ${bookId}:`, error);
                    });
            })
            .catch(error => {
                console.error("Ошибка при загрузке данных о книге:", error);
            });
    }

    function generateStars(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                stars += '<span class="star filled">★</span>';
            } else {
                stars += '<span class="star">☆</span>';
            }
        }
        return `<div class="review-stars">${stars}</div>`;
    }

    function fetchReviews() {
        fetch(`/api/books/book/${bookId}/reviews/`)
            .then(response => response.json())
            .then(data => {
                reviewsList.innerHTML = "";
                let userReviewFound = false;
                const userReview = data.find(review => review.user === username);

                if (userReview) {
                    userReviewFound = true;
                    userReviewHeader.innerHTML = `
                        <div class="user-review">
                            <strong>${userReview.user}</strong> - ${generateStars(userReview.rating)}
                            <br><br>
                            <p>${userReview.review_text}</p>
                            <br>
                            <small>Дата: ${new Date(userReview.review_date).toLocaleDateString()}</small><br>
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
                    const reviewItem = document.createElement('li');
                    reviewItem.innerHTML = `
                        <strong><a href="/users/profile/${review.user}/" class="username-link">${review.user}</a></strong></strong>  ${generateStars(review.rating)}
                        <br><br><p>${review.review_text}</p><br>
                        <small>Дата: ${new Date(review.review_date).toLocaleDateString()}</small>
                        <div class="like-button-container">
                            <button class="like-button btn" data-review-id="${review.id}"><i class="fas fa-heart"></i> <span class="like-count">0</span></button>
                        </div>
                    `;
                    reviewsList.appendChild(reviewItem);

                    // Fetch like count for the review
                    fetch(`/api/books/reviews/${review.id}/likes/`)
                        .then(response => response.json())
                        .then(data => {
                            const likeCount = data.length;
                            reviewItem.querySelector('.like-count').textContent = likeCount;

                            // Check if the user has already liked this review
                            const userLike = data.find(like => like.user === username);
                            if (userLike) {
                                reviewItem.querySelector('.like-button').classList.add('liked');
                            }
                        })
                        .catch(error => {
                            console.error("Ошибка при загрузке лайков:", error);
                        });
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

                const likeButtons = document.querySelectorAll('.like-button');
                likeButtons.forEach(button => {
                    button.addEventListener('click', () => {
                        const reviewId = button.getAttribute('data-review-id');
                        toggleLike(reviewId, button);
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

        fetch(`/api/books/book/${bookId}/reviews/`, {
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
        const rating = reviewElement.querySelector('strong').nextSibling.textContent.split('-')[1].trim();

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

        fetch(`/api/books/book/${bookId}/reviews/${reviewId}/`, {
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
        fetch(`/api/books/book/${bookId}/reviews/${reviewId}/`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).then(() => fetchReviews());
    }

    function toggleLike(reviewId, button) {
        const url = `/api/books/reviews/${reviewId}/likes/`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const userLike = data.find(like => like.user === username);
                if (userLike) {
                    // If a like already exists, delete it
                    const likeId = userLike.id;
                    const deleteUrl = `/api/books/reviews/${reviewId}/likes/${likeId}/`;

                    fetch(deleteUrl, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken'),
                        },
                    })
                    .then(response => {
                        if (response.status === 204) {
                            button.classList.remove('liked');
                            updateLikeCount(reviewId);
                        } else {
                            console.error('Ошибка при удалении лайка:', data);
                        }
                    })
                    .catch(error => {
                        console.error("Ошибка при удалении лайка:", error);
                    });
                } else {
                    // If no like exists, create a new one
                    const createData = {
                        review: reviewId,
                        user: username
                    };

                    fetch(url, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken'),
                        },
                        body: JSON.stringify(createData)
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.id) {
                            button.classList.add('liked');
                            updateLikeCount(reviewId);
                        } else {
                            console.error('Ошибка при добавлении лайка:', data);
                        }
                    })
                    .catch(error => {
                        console.error("Ошибка при отправке лайка:", error);
                    });
                }
            })
            .catch(error => {
                console.error("Ошибка при проверке существующего лайка:", error);
            });
    }

    function updateLikeCount(reviewId) {
        fetch(`/api/books/reviews/${reviewId}/likes/`)
            .then(response => response.json())
            .then(data => {
                const likeCount = data.length;
                const reviewItem = document.querySelector(`[data-review-id="${reviewId}"]`).parentElement;
                reviewItem.querySelector('.like-count').textContent = likeCount;
            })
            .catch(error => {
                console.error("Ошибка при обновлении счетчика лайков:", error);
            });
    }

    function addToReadingList(event) {
        const status = event.target.getAttribute('data-status');
        const url = `/api/users/reading_list/${username}/`;
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
