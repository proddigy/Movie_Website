from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import path, re_path
from films.views import *
from django.urls import reverse_lazy

urlpatterns = [
    path('register/', register, name='register'),

    path('login/', user_login, name='login'),

    path('logout/', user_logout, name='logout'),

    path('', HomeViews.as_view(), name='home'),

    path('genres/<slug:slug>/', MovieByGenre.as_view(), name='genres'),

    path('film/<slug:slug>/', MovieDetail.as_view(), name='films'),

    path('sessions/today', HomeViewsByDate.as_view(), name='sessions'),

    path('sessions/1', HomeViewsByDate.as_view(inputed_number=1), name='sessions_1'),
    path('sessions/2', HomeViewsByDate.as_view(inputed_number=2), name='sessions_2'),
    path('sessions/3', HomeViewsByDate.as_view(inputed_number=3), name='sessions_3'),
    path('add-movie/', add_movie, name='add_movie'),
]


