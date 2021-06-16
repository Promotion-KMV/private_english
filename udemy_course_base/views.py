from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import *


def udemy_index(request):
    homework = CourseBase.objects.all()
    context = {
        'homework': homework,
    }
    return render(request, 'udemy_course/udemy_index.html', context)


def udemy_homework(request, slug_homework):
    homework = get_object_or_404(CourseBase, slug=slug_homework)
    studywords = CourseStudyword.objects.filter(name=homework)
    book_homework = BookForHomeWork.objects.filter(name=homework)
    context = {
        'homework': homework,
        'studywords': studywords,
        'book_homework': book_homework,
    }
    return render(request, 'udemy_course/udemy_homework.html', context)


def study_words_udemy(request, homework_id):
    homework = get_object_or_404(CourseBase, id=homework_id)
    studywords = CourseStudyword.objects.filter(name=homework)
    dict_words = {}
    for word in studywords:
        dict_words[word.english_word] = word.rus_word 
    context = {
        'dict_words': dict_words,
        'homework': homework
    }

    return render(request, 'udemy_course/study_words_udemy.html', context)


# def study_words_udemy(request, word_study):
#     '''Непосредственно изучение слов организуется через vue'''
#     # study_word_name = get_object_or_404(SelfStudyWordName, id=word_study)
#     # study_words = study_word_name.study_word_name.all()
#     homework = get_object_or_404(CourseBase, id=word_study)
#     study_words = CourseStudyword.objects.filter(name=homework.word_study)
#     dict_words = {}
#     for word in study_words:
#         dict_words[word.english_word] = word.rus_word 
#     context = {
#         'dict_words': dict_words
#     }
#     return render(request, 'udemy_course/study_words_udemy.html', context)