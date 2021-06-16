from django.db import models
from english_teacher.models import *

from django.urls import reverse


class CourseBase(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, db_index=True)
    text = models.TextField()

    def __str__(serlf):
        return serlf.name

    def get_absolute_url(self):
        return f'udemy_homework/{self.slug}'

    class Meta:
        verbose_name = 'Домашнее задание к курсу'
        verbose_name_plural = 'Домашнее задания к курсу'


class CourseStudyword(models.Model):
    name = models.ForeignKey(CourseBase, on_delete=models.CASCADE, related_name='course_name')
    english_word = models.CharField(max_length=50)
    rus_word = models.CharField(max_length=50)

    def __str__(self):
        return self.english_word + ' ' + self.rus_word

    class Meta:
        verbose_name = 'Изучение слов курса'
        verbose_name_plural = 'Изучение слов курса'


class BookForHomeWork(models.Model):
    name = models.ForeignKey(CourseBase, on_delete=models.CASCADE,)
    book_name = models.ForeignKey(StudyBooks, on_delete=models.CASCADE, verbose_name='Учебник',
                                  null=True, blank=True)
    review = models.TextField(verbose_name='Задание')

