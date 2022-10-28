from django.contrib.auth.models import AbstractUser
from django.db import models

from mainapp.models import NULLABLE


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(blank=True, verbose_name='Email', unique=True)
    # age = models.PositiveSmallIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Возраст')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', **NULLABLE)
    # avatar = models.ImageField(upload_to='users', blank=True, null=True)
    avatar = models.ImageField(upload_to='users', **NULLABLE)
    # Django не работает с изображениями из коробки !
    # pip3 install pillow
    # pip3 freeze > requirements.txt

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
