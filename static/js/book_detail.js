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
                        <div class="like-dislike-buttons">
                            <button class="like-button btn" data-review-id="${review.id}"><i class="fas fa-thumbs-up"></i> <span class="like-count">0</span></button>
                            <button class="dislike-button btn" data-review-id="${review.id}"><i class="fas fa-thumbs-down"></i> <span class="dislike-count">0</span></button>
                        </div>
                    `;
                    reviewsList.appendChild(reviewItem);

                    // Fetch like and dislike counts for the review
                    fetch(`/api/bookreviewmarks/?review=${review.id}`)
                        .then(response => response.json())
                        .then(marks => {
                            const likeCount = marks.filter(mark => mark.mark === 'like').length;
                            const dislikeCount = marks.filter(mark => mark.mark === 'dislike').length;
                            reviewItem.querySelector('.like-count').textContent = likeCount;
                            reviewItem.querySelector('.dislike-count').textContent = dislikeCount;

                            // Check if the user has already marked this review
                            const userMark = marks.find(mark => mark.user === username);
                            if (userMark) {
                                if (userMark.mark === 'like') {
                                    reviewItem.querySelector('.like-button').classList.add('marked');
                                } else if (userMark.mark === 'dislike') {
                                    reviewItem.querySelector('.dislike-button').classList.add('marked');
                                }
                            }
                        })
                        .catch(error => {
                            console.error("Ошибка при загрузке оценок:", error);
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
                        const likeButton = button;
                        const dislikeButton = button.nextElementSibling;
                        toggleMark(reviewId, 'like', likeButton, dislikeButton);
                    });
                });

                const dislikeButtons = document.querySelectorAll('.dislike-button');
                dislikeButtons.forEach(button => {
                    button.addEventListener('click', () => {
                        const reviewId = button.getAttribute('data-review-id');
                        const dislikeButton = button;
                        const likeButton = button.previousElementSibling;
                        toggleMark(reviewId, 'dislike', likeButton, dislikeButton);
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
        fetch(`/api/book/${bookId}/reviews/${reviewId}/`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).then(() => fetchReviews());
    }

    function toggleMark(reviewId, markType, likeButton, dislikeButton) {
        const url = `/api/bookreviewmarks/?review=${reviewId}&user=${username}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    // If a mark already exists, update it
                    const markId = data[0].id;
                    const updateUrl = `/api/bookreviewmarks/${reviewId}/update/`;
                    const updateData = { mark: markType };

                    if (data[0].mark === markType) {
                        // If the same mark is clicked again, delete the mark
                        fetch(`/api/bookreviewmarks/${reviewId}/delete/`, {
                            method: 'DELETE',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken'),
                            },
                        })
                        .then(response => {
                            if (response.status === 204) {
                                likeButton.classList.remove('marked');
                                dislikeButton.classList.remove('marked');
                                updateMarkCounts(reviewId);
                            } else {
                                console.error('Ошибка при удалении оценки:', data);
                            }
                        })
                        .catch(error => {
                            console.error("Ошибка при удалении оценки:", error);
                        });
                    } else {
                        // If a different mark is clicked, update the mark
                        fetch(updateUrl, {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken'),
                            },
                            body: JSON.stringify(updateData)
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.id) {
                                likeButton.classList.remove('marked');
                                dislikeButton.classList.remove('marked');
                                if (markType === 'like') {
                                    likeButton.classList.add('marked');
                                } else if (markType === 'dislike') {
                                    dislikeButton.classList.add('marked');
                                }
                                updateMarkCounts(reviewId);
                            } else {
                                console.error('Ошибка при обновлении оценки:', data);
                            }
                        })
                        .catch(error => {
                            console.error("Ошибка при обновлении оценки:", error);
                        });
                    }
                } else {
                    // If no mark exists, create a new one
                    const createData = {
                        review: reviewId,
                        mark: markType
                    };

                    fetch('/api/bookreviewmarks/', {
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
                            likeButton.classList.remove('marked');
                            dislikeButton.classList.remove('marked');
                            if (markType === 'like') {
                                likeButton.classList.add('marked');
                            } else if (markType === 'dislike') {
                                dislikeButton.classList.add('marked');
                            }
                            updateMarkCounts(reviewId);
                        } else {
                            console.error('Ошибка при добавлении оценки:', data);
                        }
                    })
                    .catch(error => {
                        console.error("Ошибка при отправке оценки:", error);
                    });
                }
            })
            .catch(error => {
                console.error("Ошибка при проверке существующей оценки:", error);
            });
    }

    function updateMarkCounts(reviewId) {
        fetch(`/api/bookreviewmarks/?review=${reviewId}`)
            .then(response => response.json())
            .then(marks => {
                const likeCount = marks.filter(mark => mark.mark === 'like').length;
                const dislikeCount = marks.filter(mark => mark.mark === 'dislike').length;
                const reviewItem = document.querySelector(`[data-review-id="${reviewId}"]`).parentElement;
                reviewItem.querySelector('.like-count').textContent = likeCount;
                reviewItem.querySelector('.dislike-count').textContent = dislikeCount;
            })
            .catch(error => {
                console.error("Ошибка при обновлении счетчиков:", error);
            });
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
