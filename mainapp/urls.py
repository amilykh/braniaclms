from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig


app_name = MainappConfig.name


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('courses/', views.CoursesListView.as_view(), name='courses'),
    path('docsite/', views.DocSiteView.as_view(), name='docsite'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/<pk>/', views.NewsDetail.as_view(), name='news_detail'),
]
