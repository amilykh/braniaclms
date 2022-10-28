from django.core.management import BaseCommand

from mainapp.models import News


class Command(BaseCommand):

    def handle(self, *args, **options):
        # print('ta-da')
        """
        for i in range(10):
            News.objects.create(  # коммит в базу
                title=f'news#{i}',
                preamble=f'preamble#{i}',
                body=f'this is body for news#{i}'
            )
        """
        news_objects = []
        for i in range(10):  # лучше пачкой по 100 штук
            news_objects.append(
                News(
                    title=f'news#{i}',
                    preamble=f'preamble#{i}',
                    body=f'this is body for news#{i}'
                )
            )
        News.objects.bulk_create(news_objects)  # поднят один коннект для всех запросов
