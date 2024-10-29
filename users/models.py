from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

from books.models import Book

class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.png')
    bio = models.TextField(max_length=250, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class ReadingList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reading_list')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_entries')
    rating = models.IntegerField(null=True, blank=True)
    read_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} read {self.book.title}"

class CurrentlyReadingList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='currently_reading_list')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='currently_read_by_users')

    def __str__(self):
        return f"{self.user.username} is reading {self.book.title}"

class PlannedReadingList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='planned_reading_list')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='planned_by_users')

    def __str__(self):
        return f"{self.user.username} plans to read {self.book.title}"

class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} says "{self.review_text}" on {self.review_date}'
