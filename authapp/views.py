from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from authapp import models
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponseRedirect


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    # атрибут расширения контекста без вызова самого контекста
    extra_context = {
        'title': 'Вход пользователя'
    }


class RegisterView(TemplateView):
    template_name = 'authapp/register.html'
    # атрибут расширения контекста без вызова самого контекста
    extra_context = {
        'title': 'Регистрация пользователя'
    }

    def post(self, request, *args, **kwargs):
        try:
            print(type(request.POST))
            if all(
                    (
                        request.POST.get('username'),
                        request.POST.get('email'),
                        request.POST.get('password1'),
                        request.POST.get('password2'),
                        request.POST.get('first_name'),
                        request.POST.get('last_name'),
                        request.POST.get('password1') == request.POST.get(
                            'password2'
                        ),
                        # request.POST.get('age'),
                        # request.POST.get('avatar'),
                    )
            ):
                new_user = models.User.objects.create(
                    username=request.POST.get('username'),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    email=request.POST.get('email'),
                    age=request.POST.get('age') if request.POST.get('age')
                    else 0,
                    avatar=request.FILES.get('avatar')
                )
                new_user.set_password(request.POST.get('password1'))
                new_user.save()  # сохраняем нового пользователя
                messages.add_message(request,
                                     messages.INFO,
                                     'Регистрация прошла успешно')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    'Что-то пошло не так'
                )
                return HttpResponseRedirect(reverse('authapp:register'))

        except Exception as ex:
            messages.add_message(
                request,
                messages.WARNING,
                'Что-то пошло не так'
            )
            return HttpResponseRedirect(reverse('authapp:register'))

        # return HttpResponseRedirect(reverse('authapp:login'))  # заглушка


class CustomLogoutView(LogoutView):
    pass


class EditView(TemplateView):
    template_name = 'authapp/edit.html'

    extra_context = {
        'title': 'Регистрация пользователя'
    }

    def post(self, request, *args, **kwargs):
        # проверка того, что что-то передалось из
        if request.POST.get('username'):  # POST - формы
            # request - параметр, в который передаётся метод, в котором
            # хранится информация о том, какой пользователь, откуда он пришёл,
            # с каких страниц приходи, что у него открыалось и т.д.
            request.user.username = request.POST.get('username')
            # т.е. у нас тут лежит текущий авторизованный пользователь
            # и мы его можем достать и обратиться к любому полю

        if request.POST.get('first_name'):
            request.user.first_name = request.POST.get('first_name')

        if request.POST.get('last_name'):
            request.user.last_name = request.POST.get('last_name')

        if request.POST.get('age'):
            request.user.age = request.POST.get('age')

        if request.POST.get('email'):
            request.user.email = request.POST.get('email')

        # С паролем нужно быть очень аккуратным!
        # Для него, обычно создают, отдельную форму, которая не
        # соприкасается с остальными данными пользователя!
        #
        # if request.POST.get('password'):
        #    request.user.set_password(request.POST.get('password'))




        # а так как, обычно, это экземпляр класса, то мы можем вызывать
        # метод save()
        request.user.save()

        return HttpResponseRedirect(reverse('authapp:edit'))
