from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Movie, MovieRating
from django.urls import reverse_lazy
from django.contrib.auth.models import User
import datetime
from django.http import JsonResponse


class MovieListView(ListView):
    today = datetime.date.today()
    fifteen_days_ago = today - datetime.timedelta(days=15)
    model = Movie
    template_name = 'qfxcinema/home.html'

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        movies = Movie.objects.filter(release_date__gt=self.today)
        now_showing = Movie.objects.filter(release_date__range=(self.fifteen_days_ago, self.today))
        context = {'Movies': movies, 'now_showing_movies': now_showing}
        return context


def movie_search(request):
    name = request.GET.get('name')
    movies = Movie.objects.filter(name__icontains=name)
    context = {

        'Movies': movies
    }

    return render(request, 'qfxcinema/home.html', context)


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'qfxcinema/detail.html'
    context_object_name = 'Movie'


class MovieCreateView(CreateView):
    model = Movie
    template_name = 'qfxcinema/create.html'
    fields = ('name', 'genre', 'release_date', 'description', 'cast', 'poster', 'youtube_link')
    success_url = reverse_lazy('movie:movie-list')

    def get_context_data(self, **kwargs):
        context = super(MovieCreateView, self).get_context_data(**kwargs)
        context = {'Create': 'Create', 'form': self.get_form(), 'Create_Movie': 'Create New Movie', 'Movie': 'Movie'}

        return context


class MovieUpdateView(UpdateView):
    model = Movie
    template_name = 'qfxcinema/create.html'
    fields = '__all__'
    success_url = reverse_lazy('movie:movie-list')

    def get_context_data(self, **kwargs):
        context = super(MovieUpdateView, self).get_context_data(**kwargs)

        context = {'Update': 'Update', 'form': self.get_form(), 'Update_Movie': 'Update This Movie', }

        return context


class MovieDeleteView(DeleteView):
    model = Movie
    success_url = reverse_lazy('movie:movie-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def rating_create(request):

        if request.method == "POST":
            slug = request.POST['slug']
            user = request.POST['user']
            rating = request.POST['rating']
            movie_object = Movie.objects.get(slug=slug)
            user_object = User.objects.get(username=user)
            rating_object = MovieRating.objects.create(movie=movie_object, user=user_object, rating=rating)
            rating_object.save()
            data = {

                'rating': rating}

            return JsonResponse(data)
