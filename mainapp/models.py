from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class NewsManager(models.Manager):

    def delete(self):
        pass

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


# Create your models here.
class News(BaseModel):  # таблица новостей
    # objects = NewsManager()

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    preamble = models.CharField(max_length=1024, verbose_name='Вступление')

    body = models.TextField(verbose_name='Содержимое')
    body_as_markdown = models\
        .BooleanField(default=False,
                      verbose_name='Разметка в формате Markdown')

    def __str__(self):  # приведение типа к str
        # return f'{self.title}'
        return f"#{self.pk} {self.title}"

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class CoursesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Courses(BaseModel):
    object = CoursesManager()
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    description_as_markdown = models \
        .BooleanField(default=False,
                      verbose_name='Разметка в формате Markdown')

    cost = models.DecimalField(max_digits=8,
                               decimal_places=2,
                               verbose_name='Стоимость',
                               default=0)

    cover = models.CharField(
        max_length=25, default="no_image_svg", verbose_name='Cover'
    )

    def __str__(self) -> str:  # приведение типа к str
        # return f'{self.title}'
        return f"#{self.pk} {self.title}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(BaseModel):
    course = models.ForeignKey(Courses,
                               on_delete=models.CASCADE,
                               verbose_name='Курс')
    num = models.PositiveIntegerField(default=0, verbose_name='Номер урока')

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание', blank=True,
                                   null=True)
    description_as_markdown = models \
        .BooleanField(default=False,
                      verbose_name='Разметка в формате Markdown')

    def __str__(self) -> str:  # приведение типа к str
        return f'#{self.num} | {self.course} | {self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class CourseTeachers(BaseModel):
    course = models.ManyToManyField(Courses)  # расшивка
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')

    def __str__(self) -> str:  # приведение типа к str
        return "{0:0>3} {1} {2}".format(
            self.pk, self.last_name, self.last_name
        )

    class Meta:
        verbose_name = 'курс к учителю'
        verbose_name_plural = 'курсы к учителям'


class CourseFeedback(BaseModel):
    # RATING_FIVE = 5
    #
    # RATINGS = (
    #     (RATING_FIVE, '⭐⭐⭐⭐⭐'),
    #     (4, '⭐⭐⭐⭐'),
    #     (3, '⭐⭐⭐'),
    #     (2, '⭐⭐'),
    #     (1, '⭐'),
    # )

    RATINGS = (
        (5, '⭐⭐⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (3, '⭐⭐⭐'),
        (2, '⭐⭐'),
        (1, '⭐'),
    )

    course = models.ForeignKey(Courses, on_delete=models.CASCADE,
                               verbose_name='Курс')
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
    #                          verbose_name='Пользователь')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    rating = models.SmallIntegerField(choices=RATINGS, default=5,
                                      verbose_name='Рейтинг')
    feedback = models.TextField(verbose_name='Отзыв', default='Без отзыва')

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return f'Отзыв на {self.course} от {self.user}'
