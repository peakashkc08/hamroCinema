from django.contrib import admin
from .models import Movie, Genre, Tag, MovieRating

admin.site.register(Movie),
admin.site.register(Genre),
admin.site.register([Tag, MovieRating])
