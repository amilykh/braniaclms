# from django.contrib import messages
# from django.shortcuts import render
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
    # ******************************************
    # Модель User лежит в приложении authapp.
    # В пространстве templates в папке authapp нужно создать
    # шаблон user_form.html


# class RegisterView(TemplateView):
#     template_name = 'authapp/register.html'
#     extra_context = {
#         'title': 'Регистрация пользователя'
#     }
#
#     def post(self, request, *args, **kwargs):
#         try:
#             print(type(request.POST))
#             if all(
#                     (
#                         request.POST.get('username'),
#                         request.POST.get('email'),
#                         request.POST.get('password1'),
#                         request.POST.get('password2'),
#                         request.POST.get('first_name'),
#                         request.POST.get('last_name'),
#                         request.POST.get('password1') == request.POST.get(
#                             'password2'),
#
#                     )
#             ):
#                 new_user = User.objects.create(
#                     username=request.POST.get('username'),
#                     first_name=request.POST.get('first_name'),
#                     last_name=request.POST.get('last_name'),
#                     email=request.POST.get('email'),
#                     age=request.POST.get('age') if request.POST.get('age')
#                     else 0,
#                     avatar=request.FILES.get('avatar')
#                 )
#                 new_user.set_password(request.POST.get('password1'))
#                 new_user.save()
#                 messages.add_message(request,
#                                      messages.INFO,
#                                      'Регистрация прошла успешно')
#                 return HttpResponseRedirect(reverse('authapp:login'))
#             else:
#                 messages.add_message(
#                     request,
#                     messages.WARNING,
#                     'Что-то пошло не так'
#                 )
#                 return HttpResponseRedirect(reverse('authapp:register'))
#         except Exception as ex:
#             messages.add_message(
#                 request,
#                 messages.WARNING,
#                 'Что-то пошло не так'
#             )
#             return HttpResponseRedirect(reverse('authapp:register'))


class CustomLogoutView(LogoutView):
    pass


# class EditView(TemplateView):
#     template_name = 'authapp/edit.html'
#
#     extra_context = {
#         'title': 'Редактирование пользователя'
#     }
#
#     def post(self, request, *args, **kwargs):
#         # проверка, что что-то передалось из POST-формы
#         if request.POST.get('username'):
#             # request - это парметр, в котором хранится информация о том,
#             # какой пользователь, откуда он пришёл, с каких страниц приходил,
#             # что у него открывалось и т.д.
#             #  request.user.username - ТЕКУЩИЙ АВТОРИЗОВАННЫЙ ПОЛЬЗОВАТЕЛЬ
#             request.user.username = request.POST.get('username')
#
#         if request.POST.get('first_name'):
#             request.user.first_name = request.POST.get('first_name')
#
#         if request.POST.get('last_name'):
#             request.user.last_name = request.POST.get('last_name')
#
#         if request.POST.get('age'):
#             request.user.age = request.POST.get('age')
#
#         if request.POST.get('email'):
#             request.user.email = request.POST.get('email')
#
#         # # ОСТОРОЖНО С ПАРОЛЕМ !!!
#         # if request.POST.get('password'):
#         #     request.user.set_password(request.POST.get('username'))
#
#         request.user.save()
#         return HttpResponseRedirect(reverse('authapp:edit'))


class EditView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'authapp/edit_form .html'


    # защита от перехода по <pk>
    def get_object(self, queryset=None):
        return self.request.user

    # success_url = reverse_lazy('...')
    # в эту конструкцию pk уже не передать

    # поэтому пишем функцию
    def get_success_url(self):
        return reverse_lazy('authapp:edit', args=[self.request.user.pk])
