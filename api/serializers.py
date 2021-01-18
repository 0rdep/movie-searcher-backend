from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework import serializers
from api import models


class GetMovieSerializer(serializers.ModelSerializer):
    actors = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()

    def get_actors(self, obj):
        return obj.actors.values_list("name", flat=True)

    def get_genres(self, obj):
        return obj.genres.values_list("name", flat=True)

    def get_ratings(self, obj):
        return obj.ratings.values_list("value", flat=True)

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
        ]


class CreateUpdateMovieSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    year = serializers.CharField(required=True)
    genres = serializers.ListField(allow_empty=False, child=serializers.CharField())
    ratings = serializers.ListField(allow_empty=False, child=serializers.IntegerField())
    poster = serializers.CharField(required=True)
    content_rating = serializers.IntegerField(required=True)
    duration = serializers.CharField(required=True)
    release_date = serializers.CharField(required=True)
    average_rating = serializers.FloatField(required=True)
    original_title = serializers.CharField(allow_blank=True)
    storyline = serializers.CharField(required=True)
    actors = serializers.ListField(allow_empty=False, child=serializers.CharField())
    imdb_rating = serializers.CharField(allow_blank=True)
    posterurl = serializers.CharField(required=True)

    def create(self, validated_data):
        actors_names = validated_data.pop("actors")
        genres_names = validated_data.pop("genres")
        ratings = validated_data.pop("ratings")
        imdb_rating = validated_data.pop("imdb_rating")

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
        password = validated_data.pop('password')

        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def validate(self, data):
        model = get_user_model()
        if model.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already in use."})
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        model = get_user_model()
        users = model.objects.filter(email=data['email'])

        print(users.exists())
        print(users.get().check_password(data['password']))

        if users.exists() and users.get().check_password(data['password']):
            return data
        raise serializers.ValidationError({"error": "Wrong email or password."})

class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)