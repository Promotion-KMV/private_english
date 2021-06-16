from django.contrib import admin

from .models import *


class HomeworkInline(admin.TabularInline):
    model = BookForHomeWork
    fields = ('book_name', 'review')
    extra = 2


class UdemyStudyWordsInline(admin.TabularInline):
    model = CourseStudyword
    fields = ('english_word', 'rus_word')
    extra = 5


@admin.register(CourseBase)
class CourseBaseAdmin(admin.ModelAdmin):
    inlines = [HomeworkInline, UdemyStudyWordsInline]
    list_display = ('name', 'slug', 'text',)
    prepopulated_fields = {"slug": ("name",)}



