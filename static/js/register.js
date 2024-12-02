document.getElementById('registration-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Предотвращаем перезагрузку страницы

        const formData = new FormData(this);
        const data = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password'),
        };

        fetch('/api/users/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (response.ok) {
                // Если регистрация успешна, перенаправляем на главную страницу
                window.location.href = '/';  // URL главной страницы
            } else {
                return response.text().then(text => {
                    throw new Error(text);  // Возвращаем текст ошибки
                });
            }
        })
        .then(data => {
            // Не нужно ничего делать здесь, так как мы уже перенаправили
        })
        .catch(error => {
            document.getElementById('message').innerText = error.message;  // Сообщение об ошибке
        });
    });