from django.contrib import admin
from .models import Instructor, Module, Lecture, Student, Ping, Question, Choice

# Register your models here.
admin.site.register(Instructor)
admin.site.register(Module)
admin.site.register(Lecture)
admin.site.register(Student)
admin.site.register(Ping)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        # (None,               {'fields': ['lecture.module_id']}),
        (None,               {'fields': ['lecture_id']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'lecture_id', 'pub_date')

admin.site.register(Question, QuestionAdmin)