from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm
from authapp.models import User


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    # атрибут расширения контекста без вызова самого контекста
    extra_context = {
        'title': 'Вход пользователя'
    }


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('mainapp:index')
    # template_name = 'authapp/register.html'


class CustomLogoutView(LogoutView):
    pass


class EditView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'authapp/edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    # success_url = reverse_lazy('...')
    # в эту конструкцию pk уже не передать

    # поэтому пишем функцию
    def get_success_url(self):
        return reverse_lazy('authapp:edit', args=[self.request.user.pk])
