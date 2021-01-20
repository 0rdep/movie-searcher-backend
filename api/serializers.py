from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework import serializers
from api import models


class GetMovieSerializer(serializers.ModelSerializer):
    actors = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()

    def get_actors(self, obj):
        return obj.actors.values_list("name", flat=True)

    def get_genres(self, obj):
        return obj.genres.values_list("name", flat=True)

    def get_ratings(self, obj):
        return obj.ratings.values_list("value", flat=True)

    def get_favorite(self, obj):
        return self.context['request'].user.movie_set.filter(id=obj.id).exists()

    class Meta:
        model = models.Movie
        fields = [
            "id",
            "title",
            "year",
            "genres",
            "ratings",
            "poster",
            "content_rating",
            "duration",
            "release_date",
            "average_rating",
            "original_title",
            "storyline",
            "actors",
            "imdb_rating",
            "posterurl",
            "favorite"
        ]


class CreateUpdateMovieSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    year = serializers.CharField(required=True)
    genres = serializers.ListField(child=serializers.CharField())
    ratings = serializers.ListField(child=serializers.IntegerField())
    poster = serializers.CharField(allow_blank=True)
    content_rating = serializers.CharField(allow_blank=True)
    duration = serializers.CharField(allow_blank=True)
    release_date = serializers.CharField(allow_blank=True)
    average_rating = serializers.FloatField(required=True)
    original_title = serializers.CharField(allow_blank=True)
    storyline = serializers.CharField(allow_blank=True)
    actors = serializers.ListField(child=serializers.CharField())
    imdb_rating = serializers.CharField(allow_blank=True)
    posterurl = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        actors_names = validated_data.pop("actors")
        genres_names = validated_data.pop("genres")
        ratings = validated_data.pop("ratings")
        imdb_rating = validated_data.pop("imdb_rating")

        movies = models.Movie.objects.filter(title=validated_data["title"])
        if movies.exists():
            return movies.get()

        if imdb_rating:
            validated_data["imdb_rating"] = float(imdb_rating)
        else:
            validated_data["imdb_rating"] = 0.0

        movie = models.Movie.objects.create(**validated_data)

        for actor_name in actors_names:
            actor_entity = models.Actor.objects.get_or_create(name=actor_name)[0]
            movie.actors.add(actor_entity)

        for genre_name in genres_names:
            genre_entity = models.Genre.objects.get_or_create(name=genre_name)[0]
            movie.genres.add(genre_entity)

        for rating in ratings:
            models.Rating.objects.create(value=rating, movie=movie)

        return movie

    def update(self, movie, validated_data):
        actors_names = validated_data.pop("actors")
        genres_names = validated_data.pop("genres")
        ratings = validated_data.pop("ratings")
        imdb_rating = validated_data.pop("imdb_rating")

        for key in validated_data.keys():
            setattr(movie, key, validated_data[key])

        movie.actors.clear()
        for actor_name in actors_names:
            actor_entity = models.Actor.objects.get_or_create(name=actor_name)[0]
            movie.actors.add(actor_entity)

        movie.genres.clear()
        for genre_name in genres_names:
            genre_entity = models.Genre.objects.get_or_create(name=genre_name)[0]
            movie.genres.add(genre_entity)

        movie.ratings.all().delete()
        for rating in ratings:
            models.Rating.objects.create(value=rating, movie=movie)

        if imdb_rating:
            movie.imdb_rating = float(imdb_rating)
        else:
            movie.imdb_rating = 0.0

        movie.save()

        return movie


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        validated_data["username"] = validated_data["email"]
        password = validated_data.pop("password")

        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def validate(self, data):
        model = get_user_model()
        if model.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Email already in use."})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        model = get_user_model()
        users = model.objects.filter(email=data["email"])

        if not users.exists() or not users.get().check_password(data["password"]):
            raise serializers.ValidationError({"error": "Wrong email or password."})
        return data


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)


class GetGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ["id", "name"]
