from django.db import models
from django.urls import reverse
from datetime import datetime


class Films(models.Model):
    title = models.CharField(max_length=400, verbose_name="Название Фильма")
    description = models.TextField(blank=True, verbose_name="Описание")
    country = models.CharField(max_length=150, verbose_name="Страна выпуска")
    year_of_execution = models.IntegerField(verbose_name="Год выпуска")
    director = models.CharField(max_length=150, verbose_name="Режиссер")
    genre = models.ForeignKey("Genre", on_delete=models.PROTECT, null=True, default=1, verbose_name="Жанр")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    is_published = models.BooleanField(default=False, verbose_name="Подтвержденно")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('films', kwargs={'id': self.pk})

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['id']


class Sessions(models.Model):
    date = models.DateTimeField()
    film = models.ForeignKey("Films", related_name='sessions', on_delete=models.PROTECT, null=True)
    room = models.ForeignKey('Rooms', on_delete=models.PROTECT, null=True)



    def __str__(self):
        return f'{self.film.title} - {str(self.date)}'

    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = "Сеансы"
        ordering = ['date']


class Genre(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="Жанр")

    def get_absolute_url(self):
        return reverse('genres', kwargs={'genre_id': self.pk})

    def __str__(self):
        return self.title



    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = 'Жанры'
        ordering = ['id']

class Rooms(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название зала")
    capacity = models.IntegerField(default=50, verbose_name="Вместительность")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = 'Залы'
        ordering = ['id']

class Photos(models.Model):
    film = models.ForeignKey("Films", on_delete=models.PROTECT, null=True)
    photo_1 = models.ImageField(upload_to='gallery/%Y/%m/%d/', null=True, blank=True)
    photo_2 = models.ImageField(upload_to='gallery/%Y/%m/%d/', null=True, blank=True)
    photo_3 = models.ImageField(upload_to='gallery/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
        ordering = ['film']

class Comments(models.Model):
    film = models.ForeignKey("Films", on_delete=models.PROTECT, null=True, verbose_name='Фильм')
    name = models.CharField(verbose_name="Имя пользователя", max_length=255)
    body = models.TextField(verbose_name='Комментарий')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.film_id} - {self.name} - {self.body}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['date_added']



class MainPageCarousel(models.Model):
    photo = models.ImageField(upload_to='mainpage_photos/%Y/%m/%d/', null=True)

    def __str__(self):
        return f'photo - {self.pk}'
