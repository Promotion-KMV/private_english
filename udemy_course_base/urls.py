from django.urls import path, include

from .views import *

app_name = 'udemy_course_base'

urlpatterns = [
    path('', udemy_index, name='udemy_index'),
    path('udemy_homework/<slug:slug_homework>', udemy_homework, name='udemy_homework'),
    path('udemy_study_words/<int:homework_id>', study_words_udemy, name='study_words_udemy'),
]