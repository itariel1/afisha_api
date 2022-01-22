from django.db import models

# Create your models here.
class Cinema(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

class Review(models.Model):
    author = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema = models.ManyToManyField(Cinema)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.author