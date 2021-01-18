from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api import views

router = routers.SimpleRouter(trailing_slash=False)
router.register('movies', views.MovieViewSet, basename='movies')
router.register('auth', views.AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]