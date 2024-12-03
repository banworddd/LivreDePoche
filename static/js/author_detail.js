document.addEventListener('DOMContentLoaded', function() {
    // Функция для форматирования даты в формат dd/mm/yyyy
    function formatDate(dateString) {
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы в JavaScript начинаются с 0
        const year = date.getFullYear();
        return `${day}/${month}/${year}`;
    }

    // Извлекаем ID автора из URL-пути
    const pathParts = window.location.pathname.split('/');
    const authorId = pathParts[pathParts.length - 2]; // Предполагается, что ID находится перед последним слешем

    if (authorId) {
        // Формируем URL для запроса к API автора
        const authorApiUrl = `/api/books/author/${authorId}/`;

        // Отправляем запрос к API автора
        fetch(authorApiUrl)
            .then(response => response.json())
            .then(data => {
                // Форматируем даты
                const dateOfBirth = formatDate(data.date_of_birth);
                const dateOfDeath = data.date_of_death ? formatDate(data.date_of_death) : 'Present';

                // Получаем контейнер для отображения информации об авторе
                const authorDetails = document.getElementById('author-details');

                // Формируем HTML для отображения информации об авторе
                const authorHtml = `
                    <div class="author-info-block">
                        <img src="${data.portrait}" alt="${data.first_name} ${data.last_name}" class="author-portrait" />
                        <div class="author-name">${data.first_name} ${data.middle_name} ${data.last_name}</div>
                        <div class="author-years">${dateOfBirth} - ${dateOfDeath}</div>
                    </div>
                    <div class="bio-container">
                        <p>${data.bio}</p>
                    </div>
                    <div id="books-container" class="books-container">
                        <h2>Книги этого автора:</h2>
                        <ul id="books-list" class="books-list"></ul>
                    </div>
                `;

                // Вставляем HTML в контейнер
                authorDetails.innerHTML = authorHtml;

                // Формируем URL для запроса к API книг
                const booksApiUrl = `/api/books/bookauthorlist/?author_id=${authorId}`;

                // Отправляем запрос к API книг
                fetch(booksApiUrl)
                    .then(response => response.json())
                    .then(booksData => {
                        // Получаем контейнер для отображения книг
                        const booksList = document.getElementById('books-list');

                        // Формируем HTML для отображения книг
                        booksData.forEach(book => {
                            const bookHtml = `
                                <li class="book-block">
                                    <a href="/book/${book.id}/">
                                        <h3>${book.title}</h3>
                                    </a>
                                    <p>${book.summary}</p>
                                    <div id="rating-${book.id}" class="rating">Загрузка рейтинга...</div>
                                </li>
                            `;
                            booksList.innerHTML += bookHtml;

                            // Формируем URL для запроса к API рейтинга книги
                            const ratingApiUrl = `/api/users/rating_reviews/${book.id}/`;

                            // Отправляем запрос к API рейтинга книги
                            fetch(ratingApiUrl)
                                .then(response => response.json())
                                .then(ratingData => {
                                    const ratingContainer = document.getElementById(`rating-${book.id}`);
                                    if (ratingData.average_rating !== null) {
                                        ratingContainer.innerHTML = `Средний рейтинг: ${ratingData.average_rating.toFixed(2)}`;
                                    } else {
                                        ratingContainer.innerHTML = 'Рейтинг еще не сформирован';
                                    }
                                })
                                .catch(error => {
                                    console.error(`Error fetching rating data for book ${book.id}:`, error);
                                    const ratingContainer = document.getElementById(`rating-${book.id}`);
                                    ratingContainer.innerHTML = 'Ошибка загрузки рейтинга';
                                });
                        });
                    })
                    .catch(error => {
                        console.error('Error fetching books data:', error);
                        const booksContainer = document.getElementById('books-container');
                        booksContainer.innerHTML = '<h2>Ошибка загрузки данных о книгах</h2>';
                    });
            })
            .catch(error => {
                console.error('Error fetching author data:', error);
                const authorDetails = document.getElementById('author-details');
                authorDetails.innerHTML = '<h1 class="author-title">Ошибка загрузки данных об авторе</h1>';
            });
    } else {
        const authorDetails = document.getElementById('author-details');
        authorDetails.innerHTML = '<h1 class="author-title">ID автора не предоставлен</h1>';
    }
});
