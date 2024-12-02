document.addEventListener('DOMContentLoaded', function() {
    // Формируем URL для запроса к API
    const apiUrl = '/api/books/author/';

    // Отправляем запрос к API
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Получаем контейнер для отображения списка авторов
            const authorList = document.getElementById('author-list');
            const pageTitle = document.querySelector('.page-title');

            // Обновляем заголовок страницы
            pageTitle.textContent = 'Список авторов';

            // Очищаем список авторов
            authorList.innerHTML = '';

            // Функция для форматирования даты в формат dd/mm/yyyy
            function formatDate(dateString) {
                const date = new Date(dateString);
                const day = String(date.getDate()).padStart(2, '0');
                const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы в JavaScript начинаются с 0
                const year = date.getFullYear();
                return `${day}/${month}/${year}`;
            }

            // Проходим по каждому автору и создаем элемент списка
            data.forEach(author => {
                const dateOfBirth = formatDate(author.date_of_birth);
                const dateOfDeath = author.date_of_death ? formatDate(author.date_of_death) : 'Present';

                const authorItem = document.createElement('li');
                authorItem.className = 'author-card';
                authorItem.innerHTML = `
                    <div class="author-name"><a href="/author/${author.id}/">${author.first_name} ${author.middle_name} ${author.last_name}</a></div>
                    <div class="author-info">${dateOfBirth} - ${dateOfDeath}</div>
                    <div class="author-info">${author.summary_bio}</div>
                    <img src="${author.portrait}" alt="${author.first_name} ${author.last_name}" class="author-portrait" />
                `;
                authorList.appendChild(authorItem);
            });
        })
        .catch(error => {
            console.error('Error fetching authors:', error);
            const pageTitle = document.querySelector('.page-title');
            pageTitle.textContent = 'Error loading authors';
        });
});
