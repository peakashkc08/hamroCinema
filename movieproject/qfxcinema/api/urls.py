from django.conf.urls import include, url
from .views import MovieViewSet, GenreViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'movies', MovieViewSet)

urlpatterns = [
     url('', include(router.urls)),
     url('api-auth', include('rest_framework.urls',))
]
