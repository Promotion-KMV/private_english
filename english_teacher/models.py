from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.urls import reverse
# from datetime import date
import datetime
from sorl.thumbnail import ImageField
from .managers import CustomUserManager


class TeacherUser(models.Model):
    """Модель учителя"""
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='email')
    age = models.IntegerField(verbose_name='Возраст')
    phone = models.BigIntegerField()

    def __str__(self):
        return self.first_name + ' ' + self.email

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"


class CustomUser(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(verbose_name='Ваше имя', max_length=20)
    last_name = models.CharField(verbose_name='Ваша фамилия', max_length=20)
    age = models.IntegerField(verbose_name='Ваш возраст')
    name_teacher = models.ForeignKey(TeacherUser, on_delete=models.SET_NULL,
                                     blank=True, null=True, related_name='custom_teacher')
    is_pupil = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_message = models.BooleanField(default=False)
    count_cost_lessons = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email + ' ' + self.first_name + ' ' + self.last_name


class ReviewsTeacher(models.Model):
    """Модель отзывов"""
    name = models.CharField(max_length=30)
    ball = models.SmallIntegerField(blank=True, null=True)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class VideoMaterial(models.Model):
    """Модель видеоматериалов"""
    name = models.CharField(max_length=100,)
    video = models.FileField(upload_to='media/')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Видео урок'
        verbose_name_plural = 'Видео уроки'


class StudyBooks(models.Model):
    """Модель учебников"""
    name = models.CharField(max_length=100, unique=True)
    book = models.FileField(upload_to='books/')
    image = models.ImageField(blank=True, upload_to='books/image', verbose_name='Изображение')

    def get_absolute_url(self):
        return reverse(f'media/{self.book}')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Учебник'
        verbose_name_plural = 'Учебники'


class HomeWork(models.Model):
    """Модель домашних заданий"""

    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                    related_name='user_homework', verbose_name='Выбор ученик')
    name_user = models.CharField(max_length=50, verbose_name='Имя ученика', help_text='Указывать для семей с 2 детьми',
                                 null=True, blank=True)
    date_next_exercise = models.DateTimeField(verbose_name='Дата следующего занятия', null=True, blank=True) 
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'


class StudyAudioBook(models.Model):
    """Модель для аудиофайлов"""
    key = models.ForeignKey(StudyBooks, on_delete=models.CASCADE, null=True, blank=True, related_name='audio_book')
    # name_book = key
    name = models.CharField(max_length=50)
    audio = models.FileField(upload_to=f'books/{key}/', null=True, blank=True)

    def __str__(self):
        return self.name


class DetailHomeWork(models.Model):
    homework = models.ForeignKey(HomeWork, on_delete=models.CASCADE)
    book = models.ForeignKey(StudyBooks, on_delete=models.CASCADE, verbose_name='Учебник',
                             null=True, blank=True)
    review = models.TextField()
    audio = models.ForeignKey(StudyAudioBook, on_delete=models.CASCADE, verbose_name='Аудио',
                              null=True, blank=True)


class StudyWords(models.Model):
    """Модель изучения слов"""
    home_work = models.ForeignKey(HomeWork, on_delete=models.CASCADE,
                                  null=True, blank=True, related_name='word_homework') 
    user_name = models.SmallIntegerField(default=0)
    date = models.DateField(default=timezone.now)
    english_word = models.CharField(max_length=50)
    rus_word = models.CharField(max_length=50)

    def __str__(self):
        return self.english_word + ' ' + self.rus_word


class SelfStudyWordName(models.Model):
    """Модель имени словаря(используется для связи с самостоятельно изучаемыми словами)"""
    user_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_study_word')
    name = models.CharField(max_length=50)
    date_study = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Самостоятельное изучение'
        verbose_name_plural = 'Самостоятельное изучение'


class SelfStudyWords(models.Model):
    """Модель самостоятельного изучения слов"""
    list_words = models.ForeignKey(SelfStudyWordName, on_delete=models.CASCADE, related_name='study_word_name')
    english_word = models.TextField()
    rus_word = models.TextField()

    def __str__(self):
        return self.english_word + self.rus_word
 
    class Meta:
        verbose_name = 'Самостоятельное изучение слов'


class ModelUrlText(models.Model):
    """Модель отправки ссылки ученикам"""
    name_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='model_url_text')
    url = models.URLField(max_length=300)
    text = models.TextField(null=True, blank=True)
    date_url_create = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ссылка на занятие'
        verbose_name_plural = 'Ссылки на занятия'


class Offer(models. Model):
    """Модель предложений(пока не используется)"""
    name = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    text_offer = models.TextField()

    def __str__(self):
        return 'Предложения'

    class Meta:
        verbose_name = 'Предложениe'
        verbose_name_plural = 'Предложения'
