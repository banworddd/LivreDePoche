from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book

class CustomUser(AbstractUser):

    def __str__(self):
        return self.username

class ReadingList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)
    read_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} read {self.book.title}"

class CurrentlyReadingList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} is reading {self.book.title}"

class PlannedReadingList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} plans to read {self.book.title}"