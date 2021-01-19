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

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_serializer = self.serializer_class(serializer.instance)

        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_serializer = self.serializer_class(serializer.instance)

        return Response(response_serializer.data)


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
                "is_admin": user.is_superuser
            }
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def register(self, request):
        serializer = serializers.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)