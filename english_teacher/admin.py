from django.contrib import admin

from .models import *


class StudyWordsInline(admin.TabularInline):
    model = StudyWords
    fields = ('english_word', 'rus_word')
    extra = 5


class AudioBookInline(admin.TabularInline):
    model = StudyAudioBook
    fields = ('audio', 'name')


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    inlines = [StudyWordsInline]
    list_display = ('custom_user', 'id', 'book', 'audio', 'date')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'first_name', 'last_name', 'age', 'count_cost_lessons')


@admin.register(ReviewsTeacher)
class ReReviewsTeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'date', 'ball')


@admin.register(TeacherUser)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'age', 'phone')


@admin.register(StudyBooks)
class StudyBooksAdmin(admin.ModelAdmin):
    inlines = [AudioBookInline]
    list_display = ('name', 'book',)


@admin.register(VideoMaterial)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'video')


@admin.register(SelfStudyWords)
class SelfStudyWordsAdmin(admin.ModelAdmin):
    list_display = ('english_word', 'rus_word')


@admin.register(ModelUrlText)
class SelfStudyWordsAdmin(admin.ModelAdmin):
    list_display = ('url', 'text')
