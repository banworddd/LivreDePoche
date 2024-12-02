from django.db import models


class Author(models.Model):
    """Модель для авторов книг."""

    first_name = models.CharField(max_length=100)  # Имя автора
    middle_name = models.CharField(max_length=100, blank=True) # Отчество автора
    last_name = models.CharField(max_length=100, blank=True) # Фамилия автора
    date_of_birth = models.DateField()  # Дата рождения автора
    date_of_death = models.DateField(null=True, blank=True)  # Дата смерти автора (может быть пустой)
    summary_bio = models.TextField(max_length=100) # Сокращенная биография автора
    bio = models.TextField(max_length=500)  # Биография автора
    portrait = models.ImageField(upload_to='portraits/', default='portraits/default.png')

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        """Возвращает строковое представление автора."""
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()


class Genre(models.Model):
    """Модель для жанров книг."""

    name = models.CharField(max_length=100)  # Название жанра

    def __str__(self):
        """Возвращает строковое представление жанра."""
        return self.name


class Book(models.Model):
    """Модель для книг."""

    title = models.CharField(max_length=100)  # Заголовок книги
    authors = models.ManyToManyField(Author)  # Связь с авторами
    genre = models.ManyToManyField(Genre)  # Связь с жанрами
    summary = models.CharField(max_length=150)  # Краткое описание книги
    description = models.TextField(max_length=500)  # Полное описание книги

    def __str__(self):
        """Возвращает строковое представление книги."""
        return self.title
