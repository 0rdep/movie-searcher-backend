from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api import models
from model_bakery import baker

NEW_MOVIE = {
    "title": "Testing Movie",
    "year": "2020",
    "genres": ["Action", "Comedy", "Crime"],
    "ratings": [1],
    "poster": "testing_movie.jpg",
    "contentRating": "11",
    "duration": "PT100M",
    "releaseDate": "2020-01-18",
    "averageRating": "9.9",
    "originalTitle": "Original Testing Movie",
    "storyline": "A testing movie.",
    "actors": ["Actor 1", "Actor 2"],
    "imdbRating": 1.1,
    "posterurl": "https://google.com",
}


class CreateMoviewTestCase(APITestCase):
    def test_get_movie_list(self):
        """
        Ensure we can get the list of movies.
        """
        url = reverse("movies-list")

        baker.make(models.Movie).save()
        baker.make(models.Movie).save()
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_movie_detail(self):
        """
        Ensure we can create a new movie object.
        """
        url = reverse("movies-list")

        movie = baker.make(models.Movie)
        movie.save()

        response = self.client.get(f"{url}{movie.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], movie.title)

    def test_create_movie(self):
        """
        Ensure we can create a new movie object.
        """
        url = reverse("movies-list")

        response = self.client.post(url, NEW_MOVIE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Movie.objects.count(), 1)
        self.assertEqual(models.Movie.objects.get().title, NEW_MOVIE["title"])

    def test_update_movie(self):
        """
        Ensure we can update a new movie object.
        """
        url = reverse("movies-list")

        movie = baker.make(models.Movie)
        movie.save()

        response = self.client.put(f"{url}{movie.id}/", NEW_MOVIE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Movie.objects.count(), 1)
        self.assertEqual(models.Movie.objects.get().title, NEW_MOVIE["title"])
