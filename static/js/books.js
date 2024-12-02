document.addEventListener("DOMContentLoaded", () => {
    const API_URL = "/api/books/books_list/";  // Относительный путь
    const searchInput = document.getElementById("search-input");
    const applyFiltersButton = document.getElementById("apply-filters");
    const bookList = document.getElementById("book-list");

    // Функция для загрузки данных
    const loadBooks = (filters = {}) => {
        let url = new URL(API_URL, window.location.origin);  // Формируем полный URL
        Object.keys(filters).forEach(key => {
            if (filters[key]) url.searchParams.append(key, filters[key]);
        });

        fetch(url)
            .then(response => response.json())
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
                <p><strong>Авторы:</strong> ${book.authors.map(author => author.name).join(", ")}</p>
                <p><strong>Жанры:</strong> ${book.genre.map(genre => genre.name).join(", ")}</p>
                <p>${book.summary}</p>
            `;
            bookList.appendChild(listItem);
        });
    };

    // Обработчик события для кнопки поиска
    applyFiltersButton.addEventListener("click", () => {
        const filters = {
            search: searchInput.value.trim() || undefined,  // Приводим строку поиска к нижнему регистру
        };

        // Отфильтровываем параметры
        const nonEmptyFilters = Object.fromEntries(
            Object.entries(filters).filter(([key, value]) => value !== undefined)
        );

        loadBooks(nonEmptyFilters);
    });

    // Первоначальная загрузка данных без фильтров
    loadBooks();
});
