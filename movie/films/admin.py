from django.contrib import admin

from .models import *


class PhotosAdmin(admin.ModelAdmin):
    list_display = ('film',)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    search_fields = ('title', 'description')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'film', 'date')
    list_display_links = ('id', 'date')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'capacity')


admin.site.register(Movie, MovieAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Photos, PhotosAdmin)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(MainPageCarousel)
