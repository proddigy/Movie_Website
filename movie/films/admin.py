from django.contrib import admin

from .models import *


class PhotosAdmin(admin.ModelAdmin):
    list_display = ('film',)

class FilmsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'is_published')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    search_fields = ('title', 'description')

class SessionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date')

class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

class RoomsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'capacity')

admin.site.register(Films, FilmsAdmin)
admin.site.register(Sessions, SessionsAdmin)
admin.site.register(Genre, GenresAdmin)
admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Photos, PhotosAdmin)
admin.site.register(Comments)
admin.site.register(MainPageCarousel)