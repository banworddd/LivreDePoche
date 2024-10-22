from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre)
    summary = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.title