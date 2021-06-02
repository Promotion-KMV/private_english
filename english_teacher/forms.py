from django import forms
from english_teacher.models import *
from django.forms.widgets import TextInput


class StydyWordForm(forms.ModelForm):
    class Meta:
        model = SelfStudyWords
        fields = ['english_word', 'rus_word']
        widgets = {'english_word': TextInput(attrs={'size': 20}),
                   'rus_word': TextInput(attrs={'size': 20})}
        labels = {'english_word': 'Введите слово на английском',
                  'rus_word': 'Введите перевод'}


class StydyWordNameForm(forms.ModelForm):
    class Meta:
        model = SelfStudyWordName
        fields = ['name']
        labels = {'name': 'Придумайте название вашего словаря'}
        help_text = {'name': 'Например: части тела'}
        widgets = {'name': TextInput(attrs={'size': 40,
                   'placeholder': "Например: части тела"})}