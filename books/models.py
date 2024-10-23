from django.db import models


class Author(models.Model):
    """Модель для авторов книг."""

    name = models.CharField(max_length=100)  # Имя автора
    date_of_birth = models.DateField()  # Дата рождения
    date_of_death = models.DateField(null=True, blank=True)  # Дата смерти (может быть пустой)
    bio = models.TextField()  # Биография автора

    def __str__(self):
        """Возвращает строковое представление автора."""
        return self.name


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
    description = models.TextField()  # Полное описание книги

    def __str__(self):
        """Возвращает строковое представление книги."""
        return self.title
