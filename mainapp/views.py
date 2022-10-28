# from django.shortcuts import render
# from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    UserPassesTestMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect, JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, \
    DeleteView, DetailView, CreateView, View


from mainapp import tasks
from braniaclms import settings
from mainapp.forms import CourseFeedbackForm
from mainapp.models import News, Courses, CourseTeachers, Lesson, \
    CourseFeedback

# from datetime import datetime


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['contacts'] = [
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHcrhA',
                'city': 'Санкт‑Петербург',
                'phone': '+7-999-11-11111',
                'email': 'geeklab@spb.ru',
                'address': 'территория Петропавловская крепость, 3Ж',
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHX3xB',
                'city': 'Казань',
                'phone': '+7-999-22-22222',
                'email': 'geeklab@kz.ru',
                'address': 'территория Кремль, 11, '
                           'Казань, Республика Татарстан, Россия',
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHh9kD',
                'city': 'Москва',
                'phone': '+7-999-33-33333',
                'email': 'geeklab@msk.ru',
                'address': 'Красная площадь, 7, Москва, Россия',
            }
        ]
        return context_data

    def post(self, *args, **kwargs):
        message_body = self.request.POST.get('message_body')
        message_from = self.request.user.pk if self.request.user.is_authenticated else None
        tasks.send_feedback_to_email.delay(message_body, message_from)

        return HttpResponseRedirect(reverse_lazy('mainapp:contacts'))


# class CoursesListView(TemplateView):
#     template_name = 'mainapp/courses_list.html'
#     model = Courses

class CoursesListView(ListView):
    # template_name = 'mainapp/courses_list.html'
    model = Courses
    paginate_by = 5  # пагинация в ListView

    # # переопределяем get_queryset
    # def get_queryset(self):
    #     return super().get_queryset().filter(deleted=False)


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


# нет никаких ограничений - каждый может смотреть статьи и читать
class NewsListView(ListView):
    model = News
    paginate_by = 5  # пагинация в ListView

    # переопределяем get_queryset
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)
    

# нет никаких ограничений - каждый может смотреть статьи и читать
class NewsDetailView(DetailView):
    model = News
    # Как поступать с удалёнными новостями?
    # get_object
    # Нужно возвращать 404


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'  # все поля модели
    success_url = reverse_lazy('mainapp:news')
    # доступы - права на добавление новостей
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'  # все поля модели
    success_url = reverse_lazy('mainapp:news')
    # доступы - права на редактирование новостей
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


class CourseDetailView(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, **kwargs):
        # путь, с которого пришёл пользователь
        # /courses/?page=12
        # urllib.parse - библиотека
        #
        # /courses/12/
        #
        self.request.META.get('HTTP_REFERER')  # /courses/?page=12
        # относительно корня!!!


        context_data = super().get_context_data(**kwargs)

        context_data['course_object'] = get_object_or_404(
            Courses, pk=self.kwargs.get('pk'))
        # get_object_or_404() - возвращает или объект, или page 404 !!!

        context_data['lessons'] = Lesson.objects.filter(
            course=context_data['course_object'])

        context_data['teachers'] = CourseTeachers.objects.filter(
            course=context_data['course_object'])

        feedback_list_key = f'course_feedback_{context_data["course_object"].pk}'
        # низкоуровневое кэширование внутри контроллера
        cached_feedback_list = cache.get(
            f'course_feedback_{context_data["course_object"].pk}')
        if cached_feedback_list is None:
            # старые отзывы
            context_data['feedback_list'] = CourseFeedback.objects.filter(
                course=context_data['course_object'])
            cache.set(feedback_list_key, context_data['feedback_list'],
                      timeout=300  # время жизни кэша
                      )
        else:
            context_data['feedback_list'] = cached_feedback_list

        if self.request.user.is_authenticated:
            context_data['feedback_form'] = CourseFeedbackForm(
                course=context_data['course_object'],
                user=self.request.user
            )

        return context_data


class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_template = render_to_string(
            'mainapp/includes/feedback_card.html',
            context={'item': self.object})
        return JsonResponse({'card': rendered_template})


class LogView(UserPassesTestMixin, TemplateView):
    template_name = 'mainapp/logs.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        log_lines = []
        i = 0
        with open(settings.BASE_DIR / 'log/main_log.log') as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:
                    break
                # log_lines.append(log_file.readline())
                log_lines.insert(0, line)  # обратная сортировка
                # записываем свежие логи на самый верх

            context_data['logs'] = log_lines
        return context_data


class LogDownloadView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser


    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))
