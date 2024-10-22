from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book

class CustomUser(AbstractUser):

    def __str__(self):
        return self.username

class ReadingList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} read {self.book.title}"