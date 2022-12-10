from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import *
from django.http import HttpResponseForbidden
from datetime import datetime, timedelta
from PyMovieDb import IMDB


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('login')
        else:
            messages.error(request, "Ошибка регистрация")
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'films/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'films/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


class HomeViews(ListView):
    """List of movies"""
    model = Movie
    template_name = 'films/home_films_list.html'
    context_object_name = 'films'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'On the screen'
        context['photos'] = MainPageCarousel.objects.all()
        context['date_1'] = (datetime.today() + timedelta(1)).date()
        context['date_2'] = (datetime.today() + timedelta(2)).date()
        context['date_3'] = (datetime.today() + timedelta(3)).date()
        return context

    def get_queryset(self):
        return Movie.objects.filter(is_published=True)


class HomeViewsByDate(ListView):
    """List of films by session date"""
    model = Movie
    template_name = 'films/home_films_list.html'
    context_object_name = 'films'
    paginate_by = 8
    inputed_number = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'On the screen'
        context['photos'] = MainPageCarousel.objects.all()
        context['date_1'] = (datetime.today() + timedelta(1)).date()
        context['date_2'] = (datetime.today() + timedelta(2)).date()
        context['date_3'] = (datetime.today() + timedelta(3)).date()
        return context

    def get_queryset(self):
        pks = set()
        for item in Session.objects.filter(date=(datetime.today() + timedelta(self.inputed_number)).date()):
            pks.add(item.film_id)

        return Movie.objects.filter(pk__in=pks)


class MovieByGenre(ListView):
    """List of movies by genre"""
    model = Genre
    template_name = 'films/home_films_list.html'
    context_object_name = 'films'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Genre.objects.get(slug=self.kwargs['slug'])
        context['photos'] = MainPageCarousel.objects.all()
        context['date_1'] = (datetime.today() + timedelta(1)).date()
        context['date_2'] = (datetime.today() + timedelta(2)).date()
        context['date_3'] = (datetime.today() + timedelta(3)).date()
        return context

    def get_queryset(self):
        return Movie.objects.filter(genre=Genre.objects.get(slug=self.kwargs['slug']))


class MovieDetail(DetailView, FormMixin):
    """Movie detail view with comments"""

    model = Movie
    context_object_name = 'film_item'
    form_class = CommentForm
    template_name = 'films/films_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre_list'] = Genre.objects.filter(films=self.object)
        context['sessions'] = Session.objects.filter(film_id=self.object.id)
        context['slides'] = Photos.objects.filter(film_id=self.object.id)
        context['comments'] = Comment.objects.filter(film_id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        body = self.request.POST.get('body')
        comment = Comment.objects.create(film_id=self.object.id, name=self.request.user.username, body=body)
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('films', kwargs={'pk': self.object.pk})


def add_movie(request):

    """search by form get request"""

    if request.user.is_authenticated:
        search_class = IMDB()
        if request.method == 'GET':
            form = AddMovieForm(request.GET)
            if form.is_valid():
                search = form.cleaned_data['search']
                result = search_class.search(search)
                return render(request, 'films/add_movie.html', {'form': form, 'result': result})
        else:
            form = AddMovieForm()
        return render(request, 'films/add_movie.html', {'form': form})
    else:
        return redirect('login')
