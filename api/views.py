from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api import models
from api import serializers


class MovieViewSet(viewsets.ModelViewSet):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.GetMovieSerializer

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return serializers.CreateUpdateMovieSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queryset = queryset.filter(title__icontains=q)

        genre = self.request.query_params.get("genre")
        if genre:
            genres = models.Genre.objects.filter(name=genre)
            queryset = queryset.filter(genres__in=genres)
        return queryset.order_by("id")

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_serializer = serializers.GetMovieSerializer(
            serializer.instance, context={"request": request}
        )

        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, pk=None):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_serializer = serializers.GetMovieSerializer(
            serializer.instance, context={"request": request}
        )

        return Response(response_serializer.data)

    @action(
        detail=False, methods=["POST"], permission_classes=[permissions.IsAdminUser]
    )
    def bulk_load(self, request):
        serializer = serializers.CreateUpdateMovieSerializer(
            data=request.data, many=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"])
    def favorites(self, request):
        queryset = self.get_queryset().filter(id__in=request.user.movie_set.all())
        page = self.paginate_queryset(queryset)
        serializer = serializers.GetMovieSerializer(
            page, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["PUT", "DELETE"])
    def favorite(self, request, pk=None):
        movie = self.get_object()
        if request.method == "PUT":
            movie.user_favorites.add(self.request.user)
        else:
            movie.user_favorites.remove(self.request.user)

        movie.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["PUT", "DELETE"])
    def rate(self, request, pk=None):
        movie = self.get_object()
        
        if request.method == "PUT":
            serializer = serializers.UserRateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            rates = self.request.user.ratings.filter(movie=movie)
            if rates.exists():
                rate = rates.get()
                rate.value = serializer.validated_data["rate"]
                rate.save()
            else:
                models.Rating.objects.create(
                    movie=movie,
                    user=request.user,
                    value=serializer.validated_data["rate"],
                )
        else:
            self.request.user.ratings.filter(movie=movie).delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GetGenreSerializer
    pagination_class = None
    http_method_names = ["head", "get"]


class ActorsViewSet(viewsets.ModelViewSet):
    queryset = models.Actor.objects.all()
    serializer_class = serializers.GetGenreSerializer
    pagination_class = None
    http_method_names = ["head", "get"]


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CreateUserSerializer

    @action(detail=False, methods=["POST"])
    def login(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.pop("email")
        user = get_user_model().objects.get(email=email)

        refresh = RefreshToken.for_user(user)

        response_serializer = serializers.LoginResponseSerializer(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "is_admin": user.is_superuser,
            }
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def register(self, request):
        serializer = serializers.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)