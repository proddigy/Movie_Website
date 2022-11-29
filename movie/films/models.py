from django.db import models
from django.urls import reverse
from datetime import datetime
from django.template.defaultfilters import slugify
from random import randint


class Films(models.Model):
    title = models.CharField(max_length=400, verbose_name="Movie name")
    description = models.TextField(blank=True, verbose_name="Description")
    country = models.CharField(max_length=150, verbose_name="Country")
    year_of_execution = models.IntegerField(verbose_name="Year")
    director = models.CharField(max_length=150, verbose_name="Director")
    genre = models.ForeignKey("Genre", on_delete=models.PROTECT, null=True, default=1, verbose_name="Genre")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    is_published = models.BooleanField(default=False, verbose_name="Confirmed")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('films', kwargs={'id': self.pk})

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ['id']


class Sessions(models.Model):
    date = models.DateTimeField()
    film = models.ForeignKey("Films", related_name='sessions', on_delete=models.PROTECT, null=True)
    room = models.ForeignKey('Rooms', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.film.title} - {str(self.date)}'

    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = "Sessions"
        ordering = ['date']


class Genre(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="Genre")
    slug = models.SlugField(default=str('aka'+str(randint(100000, 999999))))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('genres', kwargs={'genre_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = 'Genres'
        ordering = ['id']


class Rooms(models.Model):
    title = models.CharField(max_length=150, verbose_name="Room")
    capacity = models.IntegerField(default=50, verbose_name="Capacity")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = 'Rooms'
        ordering = ['id']


class Photos(models.Model):
    film = models.ForeignKey("Films", on_delete=models.PROTECT, null=True)
    photo = models.ImageField(upload_to='gallery/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides(DetailView)'
        ordering = ['film']

    def __str__(self):
        return f'{self.film.title} - {self.pk}'


class Comments(models.Model):
    film = models.ForeignKey("Films", on_delete=models.PROTECT, null=True, verbose_name='Фильм')
    name = models.CharField(verbose_name="Имя пользователя", max_length=255)
    body = models.TextField(verbose_name='Комментарий')
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
