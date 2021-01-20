from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from api import views

router = routers.SimpleRouter(trailing_slash=False)
router.register("auth", views.AuthViewSet, basename="auth")
router.register("movies", views.MovieViewSet, basename="movies")
router.register("genres", views.GenresViewSet, basename="genres")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]