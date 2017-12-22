from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=30)

    # this is the model for genre

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=40)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    release_date = models.DateField(auto_now_add=False)
    description = models.TextField()
    director = models.CharField(max_length=30)
    cast = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='posters', null=True)
    youtube_link = models.TextField(blank=True, null=True)
    # the field is allowed to be blank
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    def get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Movie.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num = num + 1
        return unique_slug

    def save(self):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super(Movie, self).save()

    @property
    def get_user_rating(self):
        movie_object = Movie.objects.get(slug=self.slug)

        user_ratings_dict = movie_object.ratedmovie.all().values('user__username', 'rating')

        user_ratings_list = []

        user_ratings = ''

        for item in user_ratings_dict:
            user_ratings += '<li>' + item['user__username'] + ' has give rating of ' + str(item['rating']) + '</li>'

            user_ratings_list = user_ratings

        return user_ratings_list

    def star_percentage(self, slug, rating):
        movie_object = Movie.objects.get(slug=slug)

        rated_movie_list = movie_object.ratedmovie.all()

        total_voters = rated_movie_list.count()

        if total_voters != 0:

            filtered_rating = rated_movie_list.filter(rating=rating).count()

            rating_percentage = (filtered_rating / total_voters) * 100

            return rating_percentage

        else:

            rating_percentage = 0

            return rating_percentage

    @property
    def total_voters(self):
        movie_object = Movie.objects.get(slug=self.slug)

        rated_movie_list = movie_object.ratedmovie.all()

        total_voters = rated_movie_list.count()

        return total_voters

    @property
    def one_star_percentage(self):
        return self.star_percentage(slug=self.slug, rating=1)

    @property
    def two_star_percentage(self):
        return self.star_percentage(slug=self.slug, rating=2)

    @property
    def three_star_percentage(self):
        return self.star_percentage(slug=self.slug, rating=3)

    @property
    def four_star_percentage(self):
        return self.star_percentage(slug=self.slug, rating=4)

    @property
    def five_star_percentage(self):
        return self.star_percentage(slug=self.slug, rating=5)

    @property
    def get_rating(self):
        movie_object = Movie.objects.get(slug=self.slug)

        rated_movie_list = movie_object.ratedmovie.all()

        total_voters = rated_movie_list.count()

        total_movie_rating = 0

        if total_voters != 0:

            for rating in range(1, 6):
                total_movie_rating += (rated_movie_list.filter(rating=rating).count()) * rating

            movie_rating = total_movie_rating / total_voters

            return movie_rating

        else:

            movie_rating = 0

            return movie_rating


class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, related_name='ratedmovie', on_delete=models.CASCADE)

    user = models.ForeignKey(User, related_name='rateduser', on_delete=models.CASCADE)

    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.movie.name + self.user.username


class Tag(models.Model):
    movie = models.ManyToManyField(Movie)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(unique=True, default=0)
    gender = models.CharField(max_length=6, choices=(('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')))
    location = models.CharField(max_length=30)

    def __str__(self):
        return self.owner.username
