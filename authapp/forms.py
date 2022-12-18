# для получения ссылки на актуальную модель полльзователя
from django.contrib.auth import get_user_model
# для StyleFormMixin
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError


# Важный Mixin !
class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Проверки для работы с bootstrap
            # print(field.widget)
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-basic'
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-time'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'select2 form-control ' \
                                              'select2-multiple'
            else:
                field.widget.attrs['class'] = 'form-control'


# Сделаем форму регистрации автоматически сгенерированной
# class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
class CustomUserCreationForm(UserCreationForm):

    # Обязательно включаем класс Meta с 2-я полями
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'avatar'
        )

    def clean_age(self):
        # cleaned_data - это данные, внесённые пользователем и отвалидированные
        # по базовой валидации ( в нашем случае, age - это поле (field)
        # positive small integer (функция называется clear_field !!!)
        age = self.cleaned_data.get('age')
        if age < 18:
            raise ValidationError('Вы слишком молоды для этого сайта')
        return age


class CustomUserChangeForm(UserChangeForm):

    # Обязательно включаем класс Meta с 2-я полями
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'avatar'
        )

    def clean_age(self):
        # cleaned_data - это данные, внесённые пользователем и отвалидированные
        # по базовой валидации ( в нашем случае, age - это поле
        # positive small integer
        age = self.cleaned_data.get('age')
        if age < 18:
            raise ValidationError('Вы слишком молоды для этого сайта')
        return age
