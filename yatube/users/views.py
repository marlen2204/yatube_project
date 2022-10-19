from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    # из какого класса взять форму
    form_class = CreationForm
    # если отправка форму успешная, то перенаправляем сюда
    success_url = reverse_lazy('posts:index')
    # шаблон с полями из класса CreationView
    template_name = 'users/signup.html'
