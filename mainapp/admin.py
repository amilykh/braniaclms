from django.contrib import admin

from mainapp.models import News, Courses, Lesson, CourseTeachers

from django.utils.html import format_html

# Register your models here. (Самый простой способ)
# admin.site.register(News)
admin.site.register(Courses)
admin.site.register(Lesson)
admin.site.register(CourseTeachers)


# Более сложный способ регистрации моделей
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # столбцы, которые будут выводится
    list_display = ('pk', 'title', 'slug', 'deleted', )
    list_filter = ('deleted', 'created_at',)
    ordering = ('pk',)
    list_per_page = 5
    # в каких полях будет происходить регистрозависимый поиск
    search_fields = ('title', 'body',)
    # дополнительные действия
    actions = ('mark_as_delete',)

    def slug(self, obj):
        # return obj.title.lower().replace(' ', '-')
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.title.lower().replace(' ', '-'),
            obj.title
        )

    slug.short_description = 'Слаг'

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'
