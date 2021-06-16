from django.urls import path, include
from .views import *

app_name = 'english_teacher'

urlpatterns = [
    path('', index, name='index'),
    path('home/<int:user_id>', homework, name='homework'),
    path('books_all', books, name='books_all'),
    path('book/<int:book_id>', book, name='book'),
    path('video_all', video_all, name='video_all'),
    path('video/<int:video_id>', video, name='video'),
    path('main', main_info, name='main_info'),
    path('homework/<int:work_id>', studyhomework, name='studyhomework'),
    path('studywords_first/<int:word_study>', homework_study_words, name='studywords'),
    path('api/review', ReviewsList.as_view(), name='review_list'),
    path('<int:pk>', ReviewsDetail.as_view(), name='review_detail'),
    path('api/post', ReviewsPost.as_view(), name='review_post'),
    path('send_message/<str:sub>/<str:email>/<str:message>', send_message, name='send_message'),
    path('studywords', self_study_word, name='self_study_words'),
    path('list_study_word', list_study_word, name='list_study_word'),
    path('self_study_words/<int:word_study>', self_study_words, name='study_words'),
]

