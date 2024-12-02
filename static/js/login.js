document.getElementById('login-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Предотвращаем перезагрузку страницы

        const formData = new FormData(this);
        const data = {
            email: formData.get('email'),
            password: formData.get('password'),
        };

        fetch('/api/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.text().then(text => {
                    throw new Error(text);  // Возвращаем текст ошибки
                });
            }
        })
        .then(data => {
            // Успешная аутентификация
            document.getElementById('message').innerText = 'Успешный вход!';  // Сообщение об успехе

            // Перенаправление на главную страницу
            window.location.href = '/';  // Измените путь на нужный вам
        })
        .catch(error => {
            document.getElementById('message').innerText = error.message;  // Сообщение об ошибке
        });
    });