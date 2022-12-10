from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from random import randint
from datetime import datetime, timedelta


class Movie(models.Model):
    title = models.CharField(max_length=400, verbose_name="Movie name")
    slug = models.SlugField(max_length=400, blank=True, unique=True)
    description = models.TextField(blank=True, verbose_name="Description")
    country = models.CharField(max_length=150, verbose_name="Country")
    year_of_execution = models.IntegerField(verbose_name="Year")
    director = models.CharField(max_length=150, verbose_name="Director")
    genre = models.ManyToManyField('Genre', related_name='films')
    rating = models.CharField(max_length=10, default='0', verbose_name="Rating")
    showtime = models.CharField(max_length=100, default='0', verbose_name="Showtime")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    trailer = models.URLField(max_length=200, blank=True, verbose_name="Trailer")
    is_published = models.BooleanField(default=False, verbose_name="Confirmed")

    def __str__(self):
        return f'{self.title} ({self.year_of_execution})'

    def get_absolute_url(self):
        return reverse('films', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not Vote.objects.get(film=self):
            Vote.objects.create(film=self)
        self.slug = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)
        if not Session.objects.filter(film=self, date=datetime.today().date()):
            Session.objects.create(film=self, date=datetime.today().date(), time=datetime(2022, 1, 1, 18, 45).time(),
                                   room_id=randint(1, 3))
            Session.objects.create(film=self, date=datetime.today().date(), time=datetime(2022, 1, 1, 21, 45).time(),
                                   room_id=randint(1, 3))

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ['id']


class Session(models.Model):
    date = models.DateField(default=datetime.today().date(), verbose_name="Date")
    time = models.TimeField(default=datetime.today().time(), verbose_name="Time")
    film = models.ForeignKey("Movie", related_name='sessions', on_delete=models.PROTECT, null=True)
    room = models.ForeignKey('Room', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.film.title} {self.date} {self.time}'

    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = "Sessions"
        ordering = ['film']


class Genre(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="Genre")
    slug = models.SlugField(auto_created=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('genres', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = 'Genres'
        ordering = ['id']


class Room(models.Model):
    title = models.CharField(max_length=150, verbose_name="Room")
    capacity = models.IntegerField(default=50, verbose_name="Capacity")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = 'Rooms'
        ordering = ['id']


class Photos(models.Model):
    film = models.ForeignKey("Movie", on_delete=models.PROTECT, null=True)
    photo = models.ImageField(upload_to='gallery/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides(DetailView)'
        ordering = ['film']

    def __str__(self):
        return f'{self.film.title} - {self.pk}'


class Comment(models.Model):
    film = models.ForeignKey("Movie", on_delete=models.PROTECT, null=True, verbose_name='Movie')
    name = models.CharField(verbose_name="Username", max_length=255)
    body = models.TextField(verbose_name='Comment')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.film_id} - {self.name} - {self.body}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['date_added']


class MainPageCarousel(models.Model):
    photo = models.ImageField(upload_to='mainpage_photos/%Y/%m/%d/', null=True)

    def __str__(self):
        return f'photo - {self.pk}'

    class Meta:
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides (Main page)'
        ordering = ['pk']


class Vote(models.Model):
    film = models.OneToOneField("Movie", on_delete=models.PROTECT, null=True)
    likes = models.IntegerField(default=0, verbose_name='Likes')
    dislikes = models.IntegerField(default=0, verbose_name='Dislikes')

    def __str__(self):
        return f'{self.film.title} - {self.likes} - {self.dislikes}'

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        ordering = ['film']
