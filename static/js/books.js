document.addEventListener("DOMContentLoaded", () => {
    const API_URL = "/api/books/";  // Относительный путь
    const authorFilter = document.getElementById("author-filter");
    const genreFilter = document.getElementById("genre-filter");
    const searchInput = document.getElementById("search-input");
    const applyFiltersButton = document.getElementById("apply-filters");
    const searchButton = document.getElementById("search-button");
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

    // Функция для загрузки фильтров
    const loadFilters = () => {
        fetch(API_URL)
            .then(response => response.json())
            .then(data => {
                const authors = new Set();
                const genres = new Set();

                data.forEach(book => {
                    book.authors.forEach(author => authors.add(author.name));
                    book.genre.forEach(genre => genres.add(genre.name));
                });

                authors.forEach(author => {
                    const option = document.createElement("option");
                    option.value = author;
                    option.textContent = author;
                    authorFilter.appendChild(option);
                });

                genres.forEach(genre => {
                    const option = document.createElement("option");
                    option.value = genre;
                    option.textContent = genre;
                    genreFilter.appendChild(option);
                });
            })
            .catch(error => console.error("Ошибка при загрузке фильтров:", error));
    };

   // Убедитесь, что параметры пустого фильтра не отправляются
    applyFiltersButton.addEventListener("click", () => {
        const filters = {
            author: authorFilter.value || undefined,  // Не передавать пустое значение
            genre: genreFilter.value || undefined,    // Не передавать пустое значение
            search: searchInput.value.trim() || undefined,  // Не передавать пустое значение
        };

        // Отфильтровываем параметры
        const nonEmptyFilters = Object.fromEntries(
            Object.entries(filters).filter(([key, value]) => value !== undefined)
        );

        loadBooks(nonEmptyFilters);
    });

    // Событие на кнопку поиска
    searchButton.addEventListener("click", () => {
        const filters = {
            search: searchInput.value.trim().toLowerCase(), // Приводим строку поиска к нижнему регистру
        };
        loadBooks(filters);
    });

    // Первоначальная загрузка данных
    loadFilters();
    loadBooks();
});
