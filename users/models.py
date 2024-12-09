from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from books.models import Book

class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    bio = models.TextField(max_length=250, blank=True, null=True)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()  # Преобразуем email в нижний регистр
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class FriendsList(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('waiting', 'Waiting'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friends_list_user')
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friends_list_friend')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')

    class Meta:
        unique_together = ('user', 'friend', 'status')
        verbose_name_plural = 'Запросы в друзья'
        verbose_name = 'Запросы в друзья'


class ReadingList(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('currently_reading', 'Currently Reading'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reading_list')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_entries')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    read_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'book', 'status')
        verbose_name = "Reading List Entry"
        verbose_name_plural = "Reading List Entries"

    def __str__(self):
        return f"{self.user.username} - {self.status} '{self.book.title}'"

    @property
    def rating(self):
        review = BookReview.objects.filter(user=self.user, book=self.book).first()
        return review.rating if review else None


class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    review_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # Уникальное ограничение для пользователя и книги

    def __str__(self):
        return f'{self.user.username} says "{self.review_text}" on {self.review_date}'


class ReviewLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.ForeignKey(BookReview, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')  # Уникальное ограничение для пользователя и обзора

    def __str__(self):
        return f'{self.user.username} liked {self.review.user.username}\'s review on {self.review.review_date}'

