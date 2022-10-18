from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

# из файла apps.py
# app_name = 'mainapp'
app_name = MainappConfig.name

urlpatterns = [
    # '' - пустой паттерн, который будет ссылаться на корень сайта
    # views.hello_world -  ссылка на функцию, котора будет отрабатывать
    # name - параметр необходим будет позже для быстрого доступа к url-ам
    path('', views.hello_world, name='hello_world'),
    path('<str:word>/', views.blog),
    # path('blog/', views.blog),
]
