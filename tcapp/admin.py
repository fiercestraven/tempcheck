from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Module, Lecture, Ping, Question, Choice, User

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

class UserAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'username', 'email', 'password', 'is_staff']
    list_filter = ('is_staff',)

# Register your models here.
admin.site.register(Module)
admin.site.register(Lecture)
admin.site.register(Ping)
admin.site.register(Question, QuestionAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)