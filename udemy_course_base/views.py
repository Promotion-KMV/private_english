from django.shortcuts import render, get_object_or_404
# from .models import *


# def udemy_index(request):
#     homework = CourseBase.objects.all()
#     context = {
#         'homework': homework,
#     }
#     return render(request, 'udemy_course/udemy_index.html', context)


# def udemy_homework(request, slug_homework):
#     homework = get_object_or_404(CourseBase, slug=slug_homework)
#     studywords = CourseStudyword.objects.filter(name=homework)
#     context = {
#         'homework': homework,
#         'studywords': studywords,
#     }
#     return render(request, 'udemy_course/udemy_homework.html', context)
