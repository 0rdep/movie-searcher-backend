from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255)


class Actor(models.Model):
    name = models.CharField(max_length=255)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre)
    poster = models.CharField(max_length=255)
    content_rating = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    release_date = models.CharField(max_length=255)
    average_rating = models.FloatField()
    original_title = models.CharField(max_length=255)
    storyline = models.CharField(max_length=255)
    actors = models.ManyToManyField(Actor)
    imdb_rating = models.FloatField(max_length=255)
    posterurl = models.CharField(max_length=255)
    user_favorites = models.ManyToManyField(User)


class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name="ratings", on_delete=models.CASCADE)
    value = models.IntegerField()
    user = models.ForeignKey(User, related_name="ratings", on_delete=models.SET_NULL, null=True)
