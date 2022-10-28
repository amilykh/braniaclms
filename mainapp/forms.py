from django import forms
from mainapp.models import CourseFeedback


class CourseFeedbackForm(forms.ModelForm):

    class Meta:
        model = CourseFeedback
        fields = ('course', 'user', 'rating', 'feedback')
        widgets = {
            'course': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'rating': forms.RadioSelect()
        }

    # Мы принимаем поля 'course' 'user', но не показываем пользователю.
    # Поэтому их нужно предустановить.
    def __init__(self, *args, course=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)  # !!! только *args и **kwargs
        if course and user:  # проверяем, что и пользователь, и курс в наличии!
            self.fields['course'].initial = course.pk
            self.fields['user'].initial = user.pk
