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
        // Формируем URL для запроса к API
        const apiUrl = `/api/books/author/${authorId}/`;

        // Отправляем запрос к API
        fetch(apiUrl)
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
                `;

                // Вставляем HTML в контейнер
                authorDetails.innerHTML = authorHtml;
            })
            .catch(error => {
                console.error('Error fetching author data:', error);
                const authorDetails = document.getElementById('author-details');
                authorDetails.innerHTML = '<h1 class="author-title">Error loading author data</h1>';
            });
    } else {
        const authorDetails = document.getElementById('author-details');
        authorDetails.innerHTML = '<h1 class="author-title">Author ID not provided</h1>';
    }
});
