from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from api import models
from model_bakery import baker
from django.contrib.auth.models import User

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


class MovieTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@admin.com", password="admin"
        )

        self.active_user = User.objects.create_user(
            username="inactive",
            email="inactive@inactive.com",
            password="inactive",
            is_active=False,
        )

        self.active_user = User.objects.create_user(
            username="active", email="active@active.com", password="active"
        )

    def test_get_movie_list(self):
        """
        Ensure we can get the list of movies.
        """
        url = reverse("movies-list")

        baker.make(models.Movie).save()
        baker.make(models.Movie).save()

        refresh = RefreshToken.for_user(self.active_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_get_movie_detail(self):
        """
        Ensure we can create a new movie object.
        """
        url = reverse("movies-list")

        movie = baker.make(models.Movie)
        movie.save()

        refresh = RefreshToken.for_user(self.active_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.get(f"{url}/{movie.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], movie.title)

    def test_create_movie(self):
        """
        Ensure we can create a new movie object.
        """
        url = reverse("movies-list")

        refresh = RefreshToken.for_user(self.active_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
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

        refresh = RefreshToken.for_user(self.active_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.put(f"{url}/{movie.id}", NEW_MOVIE)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Movie.objects.count(), 1)
        self.assertEqual(models.Movie.objects.get().title, NEW_MOVIE["title"])

    def test_favorite_movie(self):
        """
        Ensure we add a movie to favorite list
        """
        url = reverse("movies-list")

        movie = baker.make(models.Movie)
        movie.save()

        refresh = RefreshToken.for_user(self.active_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.put(f"{url}/{movie.id}/favorite")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.active_user.movie_set.count(), 1)

    def test_unfavorite_movie(self):
        """
        Ensure we can remove a movie from favorite list
        """
        url = reverse("movies-list")

        movie = baker.make(models.Movie)
        movie.user_favorites.add(self.active_user)
        movie.save()

        refresh = RefreshToken.for_user(self.active_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.delete(f"{url}/{movie.id}/favorite")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.active_user.movie_set.count(), 0)

    def test_rate_movie(self):
        """
        Ensure we can rate a movie
        """
        url = reverse("movies-list")

        movie = baker.make(models.Movie)
        movie.save()

        refresh = RefreshToken.for_user(self.active_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.put(f"{url}/{movie.id}/rate", {"rate": 0})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.active_user.ratings.count(), 1)

    def test_delete_rate_movie(self):
        """
        Ensure we can delete a movie rate
        """
        url = reverse("movies-list")

        movie = baker.make(models.Movie)
        movie.save()

        models.Rating.objects.create(
            movie=movie,
            user=self.active_user,
            value=0,
        )

        refresh = RefreshToken.for_user(self.active_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.delete(f"{url}/{movie.id}/rate")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.active_user.ratings.count(), 0)

    def test_bulk_load(self):
        """
        Ensure we can bulk load
        """
        url = reverse("movies-bulk-load")

        first_movie = {**NEW_MOVIE, "title": "first-movie"}
        second_movie = {**NEW_MOVIE, "title": "second-movie"}

        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.post(url, [first_movie, second_movie])

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Movie.objects.count(), 2)


class GenreTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@admin.com", password="admin"
        )

        self.active_user = User.objects.create_user(
            username="inactive",
            email="inactive@inactive.com",
            password="inactive",
            is_active=False,
        )

        self.active_user = User.objects.create_user(
            username="active", email="active@active.com", password="active"
        )

    def test_get_genres_list(self):
        """
        Ensure we can get the list of genres.
        """
        url = reverse("genres-list")

        baker.make(models.Genre).save()
        baker.make(models.Genre).save()

        refresh = RefreshToken.for_user(self.active_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class AuthTestCase(APITestCase):
    def test_register(self):
        """
        Ensure we can register
        """
        url = reverse("auth-register")
        email = "test@test.com"
        password = "123456"

        response = self.client.post(url, {"email": email, "password": password})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_login(self):
        """
        Ensure we can login
        """
        url = reverse("auth-login")
        email = "test@test.com"
        password = "123456"
        User.objects.create_user(username="test", email=email, password=password)

        response = self.client.post(url, {"email": email, "password": password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
