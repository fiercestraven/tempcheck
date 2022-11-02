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
        (None,               {'fields': ['lecture']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'lecture', 'pub_date')

class UserAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'username', 'email', 'password', 'is_staff']
    list_filter = ('is_staff',)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')

class ModuleAdmin(admin.ModelAdmin):
    fields = ['module_name', 'module_description', 'instructor', 'is_active']
    list_filter = ('is_active',)
    list_display = ('module_name', 'module_description', 'instructor', 'is_active')

class LectureAdmin(admin.ModelAdmin):
    fields = ['module', 'lecture_name', 'lecture_description', 'lecture_date']
    list_display = ('module', 'lecture_name', 'lecture_description', 'lecture_date')

class PingAdmin(admin.ModelAdmin):
    fields = ['student', 'lecture', 'ping_date']
    list_display = ('student', 'lecture', 'ping_date')

# Register your models here.
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Ping, PingAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)