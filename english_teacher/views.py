from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from rest_framework import generics
from .serializers import ReviewSerializer
from django.utils.encoding import *
from django.core.mail import EmailMessage
from django.forms import formset_factory
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
import datetime


def developer(request):
    return render(request, 'develop/developer.html')


def books(request):
    """Страница отображения всех учебников"""
    search_query = request.GET.get('search_books', '')
    if search_query:
        books = StudyBooks.objects.filter(name__icontains=search_query)
    else:
        books = StudyBooks.objects.all()
    context = {
        'books': books,
    }
    return render(request, 'books_all.html', context)


def book(request, book_id):
    """Страница отображения учебника с аудио()если есть"""
    book = get_object_or_404(StudyBooks, id=book_id)
    search_query = request.GET.get('search_audio', '')
    if search_query:
        all_audio = StudyAudioBook.objects.filter(key=book_id, name__icontains=search_query)
    else:
        all_audio = StudyAudioBook.objects.filter(key=book_id)
    context = {
        'all_audio': all_audio,
        'book': book,
    }
    return render(request, 'book.html', context)


@login_required
def video_all(request):
    """Страница отражения всех видео лекций"""
    all_video = VideoMaterialYoutube.objects.all().order_by('name')
    context = {
        'all_video': all_video,
    }
    return render(request, 'video_all.html', context)

@login_required
def video(request, video_id):
    """Страница отражения выбранной видео лекции"""
    video = get_object_or_404(VideoMaterialYoutube, id=video_id)
    context = {
        'video': video
    }
    return render(request, 'video.html', context)


def index(request):
    """Главная страница"""
    if request.user.is_authenticated or request.user.is_staff:
        return HttpResponseRedirect(reverse_lazy('english_teacher:main_info'))

    return render(request, 'index.html')


def main_info(request):

    """ Главная страница зарегистрированного пользователя """

    home_work = HomeWork.objects.filter(custom_user=request.user).last()
    # date = datetime.datetime.now()
    date = datetime.datetime.today()
    url_user = ''
    url = ModelUrlText.objects.filter(name_user=request.user).last()
    if not url:
        url = ''
    else:
        if date.timestamp() - url.date_url_create.timestamp() < 1800:
            url_user = ModelUrlText.objects.filter(name_user=request.user).last()

    all_exercise = HomeWork.objects.filter(date_next_exercise__gte=date).order_by('date_next_exercise')
    context = {
        'url_user': url_user,
        'homework': home_work,
        'date': date,
        'all_exercise': all_exercise
    }
    return render(request, 'main_info.html', context)


def homework(request, user_id):
    """Выбор домашнего задания ученика"""
    home_work = HomeWork.objects.filter(custom_user=request.user).order_by('-date')[:5]
    
    context = {
        'homework': home_work,
    }
    return render(request, 'homework/homework.html', context)

@login_required
def studyhomework(request, work_id):
    """Домашнее задание"""
    home_work = get_object_or_404(HomeWork, id=work_id)
    study_words = StudyWords.objects.filter(home_work=work_id)
    study_home_work = DetailHomeWork.objects.filter(homework=home_work)
    context = {
        'homework': home_work,
        'studywords': study_words,
        'studyhomework': study_home_work,
    }
    return render(request, 'homework/studyhomework.html', context)


def homework_study_words(request, word_study):
    """Изучение слов заданных преподавателем"""
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
    try:
        email.send(fail_silently=False)
        return HttpResponse('Это сообщение успешно отправленно!')
    except:
        return HttpResponse('Сообщение не отправлено ошибка сервера')
    # logger.debug('hello!')


def self_study_word(request):
    """ Добавление слов для самостоятельного изучения"""
    user_name = request.user.id
    study_words = formset_factory(StydyWordForm, extra=10)
    SelfStudyWordNameView = formset_factory(StydyWordNameForm, extra=1)
    if request.method == 'POST':
        formset = study_words(request.POST)
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

    formset = study_words()
    formset_name = SelfStudyWordNameView()
    context = {
        'formset': formset,
        'formset_name': formset_name,
        }
    return render(request, 'study_words/self_study_words.html', context)


def list_study_word(request):
    """Выбор словаря для повторного изучения"""
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
    """Непосредственно изучение слов организуется через vue"""
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
