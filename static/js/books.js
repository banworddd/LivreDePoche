document.addEventListener("DOMContentLoaded", () => {
    const API_URL = "/api/books/books_list/";  // Относительный путь
    const bookList = document.getElementById("book-list");

    // Функция для загрузки данных
    const loadBooks = () => {
        fetch(API_URL)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка при загрузке данных');
                }
                return response.json();
            })
            .then(data => {
                renderBooks(data);
            })
            .catch(error => {
                console.error("Ошибка при загрузке книг:", error);
                bookList.innerHTML = "<li>Ошибка загрузки данных.</li>";
            });
    };

    // Функция для рендеринга списка книг
    const renderBooks = (books) => {
        bookList.innerHTML = "";
        if (books.length === 0) {
            bookList.innerHTML = "<li>Ничего не найдено.</li>";
            return;
        }
        books.forEach(book => {
            const listItem = document.createElement("li");
            listItem.classList.add("book-card");  // Добавляем класс для стилизации карточек
            listItem.innerHTML = `
                <h4 class="book-title"><a href="/book/${book.id}/">${book.title}</a></h4>
                <p><strong>Авторы:</strong> ${book.authors.map(author => `${author.first_name} ${author.middle_name} ${author.last_name}`.trim()).join(", ")}</p>
                <p><strong>Жанры:</strong> ${book.genre.map(genre => genre.name).join(", ")}</p>
                <p>${book.summary}</p>
                <div id="rating-${book.id}" class="rating">Загрузка рейтинга...</div>
            `;
            bookList.appendChild(listItem);

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
                    console.error(`Ошибка при загрузке рейтинга для книги ${book.id}:`, error);
                    const ratingContainer = document.getElementById(`rating-${book.id}`);
                    ratingContainer.innerHTML = 'Ошибка загрузки рейтинга';
                });
        });
    };

    // Первоначальная загрузка данных без фильтров
    loadBooks();
});
