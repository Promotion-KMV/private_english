from django.contrib import admin

from .models import *


class UdemyStudyWordsInline(admin.TabularInline):
    model = CourseStudyword
    fields = ('english_word', 'rus_word')
    extra = 5


@admin.register(CourseBase)
class CourseBaseAdmin(admin.ModelAdmin):
    inlines = [UdemyStudyWordsInline]
    list_display = ('name', 'slug', 'text',)
    prepopulated_fields = {"slug": ("name",)}

