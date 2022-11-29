from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import ModelFormMixin
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import *
from django.http import HttpResponseForbidden
from datetime import datetime, timedelta


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
    model = Films
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
        return Films.objects.filter(is_published=True)


class HomeViewsByDate(ListView):
    model = Films
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
        pks = []
        for item in Sessions.objects.filter(date__month=datetime.today().month,
                                            date__day=(datetime.today() + timedelta(self.inputed_number)).day):
            pks.append(item.film_id)

        return Films.objects.filter(pk__in=pks)


class FilmsByGenre(ListView):
    model = Films
    template_name = 'films/home_films_list.html'
    context_object_name = 'films'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Genre.objects.get(pk=self.kwargs['genre_id'])
        context['photos'] = MainPageCarousel.objects.all()
        context['date_1'] = (datetime.today() + timedelta(1)).date()
        context['date_2'] = (datetime.today() + timedelta(2)).date()
        context['date_3'] = (datetime.today() + timedelta(3)).date()
        return context

    def get_queryset(self):
        return Films.objects.filter(genre_id=self.kwargs['genre_id'], is_published=True)


def film_detail_view(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            body = request.POST.get('body')
            comment = Comments.objects.create(film_id=id, name=request.user.username, body=body)
            comment.save()
            return redirect('films', id)
    else:
        form = CommentForm()

    context = {
        'film_item': Films.objects.filter(id=id).first(),
        'form': form,
        'sessions': Sessions.objects.filter(film_id=id),
        'slides': Photos.objects.filter(film_id=id),
        'comments': Comments.objects.filter(film_id=id)
    }
    return render(request, 'films/films_detail.html', context)


class FilmDetailView(DetailView, ModelFormMixin):
    model = Films
    context_object_name = 'film_item'
    form_class = CommentForm
    template_name = 'films/films_detail.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = Photos.objects.get(film_id=self.kwargs['pk'])
        context['sessions'] = Sessions.objects.filter(film_id=self.kwargs['pk'])
        context['comments'] = Comments.objects.filter(film_id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.film_id = self.kwargs['pk']
        form.instance.name = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('film', self.kwargs['pk'])
