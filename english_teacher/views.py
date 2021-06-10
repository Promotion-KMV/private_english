from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import generics
from english_teacher.serializers import ReviewSerializer
from django.utils.encoding import *
from django.core.mail import EmailMessage
from django.forms import formset_factory
from django.contrib.sites.shortcuts import get_current_site

from .models import *
from .forms import *
import datetime


def books(request):
    """Страница отображения всех учебников"""
    books = StudyBooks.objects.all()
    context = {
        'books': books,
    }
    return render(request, 'books_all.html', context)


def book(request, book_id):
    """Страница отображения учебника с аудио()если есть"""
    book = get_object_or_404(StudyBooks, id=book_id)
    all_audio = StudyAudioBook.objects.filter(name_book=book_id)
    context = {
        'all_audio': all_audio,
        'book': book,
    }
    return render(request, 'book.html', context)


def video_all(request):
    """Страница отражения всех видеолекций"""
    all_video = VideoMaterial.objects.all()
    context = {
        'all_video': all_video,
    }
    return render(request, 'video_all.html', context)


def video(request, video_id):
    """Страница отражения выбранной видеолекции"""
    video=get_object_or_404(VideoMaterial, id=video_id)
    context = {
        'video': video
    }
    return render(request, 'video.html', context)


def index(request):
    """Главная страница"""
    if request.user.is_authenticated:
        return render(request, 'main_info.html',) 

    return render(request, 'index.html')


def main_info(request):
    '''Главная страница зарегестрированного пользователя'''
    homework = HomeWork.objects.filter(custom_user=request.user).last()
    date = datetime.datetime.now()
    url_user = ''
    url = ModelUrlText.objects.filter(name_user=request.user).last()
    if not url :
        url = ''
    else:
        if date.timestamp() - url.date_url_create.timestamp() < 1800:
            url_user = ModelUrlText.objects.filter(name_user=request.user).last()

    all_ecxercise = homework = HomeWork.objects.filter(date_next_exercise__gte=date).order_by('date_next_exercise')
    context = {
        'url_user': url_user,
        'homework': homework,
        'date': date,
        'all_ecxercise': all_ecxercise
    }
    return render(request, 'main_info.html', context)


def homework(request, user_id):
    '''Выбор домашнего задания ученика'''
    homework = HomeWork.objects.filter(custom_user=request.user)[:5]
    
    context = {
        'homework': homework,
    }
    return render(request, 'homework/homework.html', context)


def studyhomework(request, work_id):
    '''Домашнее задание'''
    homework = get_object_or_404(HomeWork, id=work_id)
    studywords = StudyWords.objects.filter(home_work=work_id)
    studybook = get_object_or_404(StudyBooks, name=homework.book)
    studyaudio = StudyAudioBook.objects.all()
    book_url = studybook.book.url
    audio = StudyAudioBook.objects.all()
    video = VideoMaterial.objects.all()
    context = {
        'homework': homework,
        'studywords': studywords,
        'studybook': studybook,
        'book_url': book_url,
        'audio': audio,
        'studyaudio': studyaudio,
        'video': video,

    }
    return render(request, 'homework/studyhomework.html', context)


def homework_study_words(request, word_study):
    '''Изучение слов заданных преподавателем'''
    studywords = StudyWords.objects.filter(home_work=word_study)
    dict_words = {}
    for word in studywords:
        dict_words[word.english_word] = word.rus_word 
    context = {
        'studywords': studywords,
        'dict_words': dict_words,

    }
    return render(request, 'homework/homework_study_words.html', context)


def send_message(request, sub, email, message):
    """Функция отправки сообщения используется из vue"""
    if sub == 'review':
        theme = 'Отзыв от пользователя' + ' ' +  email
    else:
        theme = 'Сообщение от пользователя' + ' ' +  email
    email = EmailMessage(
        subject=theme,
        body=message,
        from_email='privatenglishtutor@yandex.ru',
        to=['privatenglishtutor@yandex.ru',]
    )
    email.send()


def self_study_word(request):
    ''' Добавление слов для самостоятельного изучения'''
    user_name = request.user.id
    StudyWords = formset_factory(StydyWordForm, extra=10)
    SelfStudyWordNameView = formset_factory(StydyWordNameForm, extra=1)
    if request.method == 'POST':
        formset = StudyWords(request.POST)
        name_form = 'Без названия'
        if formset.is_valid():
            if len(request.POST['form-0-name']) <= 0:
                SelfStudyWordName.objects.all().create(user_name=CustomUser.objects.get(id=request.user.id),
                                                       name=name_form)
            else:
                SelfStudyWordName.objects.all().create(user_name=CustomUser.objects.get(id=request.user.id),
                                                       name=request.POST['form-0-name'])
            last_words_name = SelfStudyWordName.objects.filter(user_name=request.user)
            word_name_save = last_words_name.latest('id')
            for form_set in formset:
                form = form_set.save(commit=False)
                if form.english_word != '':
                    form.list_words = word_name_save
                    form.save()
            study_word = word_name_save
            return HttpResponseRedirect(reverse_lazy('english_teacher:study_words', args=(study_word.id,)))

    formset = StudyWords()
    formset_name = SelfStudyWordNameView()
    context = {
        'formset': formset,
        'formset_name': formset_name,
        }
    return render(request, 'study_words/self_study_words.html', context)


def list_study_word(request):
    '''Выбор словаря для повторного изучения'''
    search_query_start = request.GET.get('search_date_start', '')
    search_query_end = request.GET.get('search_date_end', '')
    if search_query_start and search_query_end:
        list_words_name = SelfStudyWordName.objects.filter(user_name=request.user.id, 
                                                           date_study__gte=search_query_start,
                                                           date_study__lte=search_query_end).order_by('-pk')
    elif search_query_start:
        list_words_name = SelfStudyWordName.objects.filter(user_name=request.user.id,
                                                           date_study=search_query_start).order_by('-pk')
    else:
        list_words_name = SelfStudyWordName.objects.filter(user_name=request.user.id).order_by('-pk')[:3]
        
    list_words = SelfStudyWords.objects.all()
    context = {
        'list_words': list_words, 
        'list_words_name': list_words_name,
    }
    return render(request, 'study_words/list_study_word.html', context)


def self_study_words(request, word_study):
    '''Непосредственно изучение слов организуется через vue'''
    study_word_name = get_object_or_404(SelfStudyWordName, id=word_study)
    study_words = study_word_name.study_word_name.all()
    dict_words = {}
    for word in study_words:
        dict_words[word.english_word] = word.rus_word 
    context = {
        'dict_words': dict_words
    }
    return render(request, 'study_words/study_words.html', context)


'''Блок DRF'''


class ReviewsList(generics.ListAPIView):
    queryset = ReviewsTeacher.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        reviews = ReviewsTeacher.objects.all()
        return reviews


class ReviewsDetail(generics.RetrieveAPIView):
    queryset = ReviewsTeacher.objects.all()
    serializer_class = ReviewSerializer


class ReviewsPost(generics.ListCreateAPIView):
    queryset = ReviewsTeacher.objects.all()
    serializer_class = ReviewSerializer