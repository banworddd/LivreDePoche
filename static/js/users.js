document.addEventListener("DOMContentLoaded", function() {
    const userList = document.getElementById('user-list');
    const searchInput = document.getElementById('search-input');

    function fetchUsers() {
        fetch('/api/user_list/')
            .then(response => response.json())
            .then(data => {
                renderUsers(data);
            })
            .catch(error => {
                console.error("Ошибка при загрузке пользователей:", error);
            });
    }

    function renderUsers(users) {
        userList.innerHTML = ""; // Очищаем список перед добавлением новых пользователей
        users.forEach(user => {
            const listItem = document.createElement('li');
            listItem.classList.add('user-list-item');
            listItem.innerHTML = `
                <div class="user-list-info">
                    <img src="${user.avatar}" alt="${user.username}'s avatar" class="user-list-avatar">
                    <div class="user-list-details">
                        <h2 class="user-list-username"><a href="/users/profile/${user.username}/" class="username-link">${user.username}</a></h2>
                        <p class="user-list-bio">${user.bio || 'Статус отсутствует'}</p>
                    </div>
                </div>
            `;
            userList.appendChild(listItem);
        });
    }

    function filterUsers(query) {
        fetch('/api/user_list/')
            .then(response => response.json())
            .then(data => {
                const filteredUsers = data.filter(user =>
                    user.username.toLowerCase().includes(query.toLowerCase())
                );
                renderUsers(filteredUsers);
            })
            .catch(error => {
                console.error("Ошибка при загрузке пользователей:", error);
            });
    }

    searchInput.addEventListener('input', function() {
        const query = searchInput.value;
        if (query) {
            filterUsers(query);
        } else {
            fetchUsers();
        }
    });

    fetchUsers();
});
