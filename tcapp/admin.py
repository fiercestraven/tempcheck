from io import TextIOWrapper
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.urls import path, reverse
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
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

class csvImportForm(forms.Form):
    csv_upload = forms.FileField()

class UserAdmin(UserAdmin):
    # have to use UserAdmin instead of modelAdmin and add_fieldsets because of overriding the built-in User model forms: https//docs.djangoproject.com/en/4.1/topics/auth/customizing/
    add_fieldsets = [
        ('Account info', {'fields': ['username', 'password1', 'password2', 'is_staff']}),
        ('Personal info', {"fields": ("first_name", "last_name", "email")}),
    ]
    list_filter = ('is_staff',)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')

    # defining url path for csv upload: https://www.youtube.com/watch?v=BLxCnD5-Uvc
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            # below csv_upload is from the csvImportForm function above
            csv_file = request.FILES["csv_upload"]
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded.')
                return HttpResponseRedirect(request.path_info)
            # rows = TextIOWrapper(csv_file, encoding="utf-8", newline="")
            file_data = csv_file.read().decode("utf-8")
            # split into list of lines
            csv_data = file_data.split("\n")
            # iterate over lines and split into fields
            
            row_count = 0
            form_errors = []
            for x in csv_data:
                row_count +=1
                # fv - note: here, put into a form and then run validation - if working, can delete from fields=x.split(",")
                form = csvImportForm(x)
                if not form.is_valid():
                    form_errors = form.errors
                    break
                form.save()
                # below is current code (non-form), working:
                fields = x.split(",")
                # note - username in the Django model is unique; will use that and let it auto-fill pk
                created = User.objects.update_or_create(
                    username = fields[0],
                    first_name = fields[1],
                    last_name = fields[2],
                    email = fields[3],
                    is_staff = fields[4]
                )
            url = reverse('admin:auth_user_changelist')
            return HttpResponseRedirect(url)
        form = csvImportForm
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

class ModuleAdmin(admin.ModelAdmin):
    fields = ['module_shortname', 'module_name', 'module_description', 'instructor', 'is_active']
    list_filter = ('is_active',)
    list_display = ('module_shortname', 'module_name', 'module_description', 'instructor', 'is_active')

class LectureAdmin(admin.ModelAdmin):
    fields = ['module', 'lecture_name', 'lecture_description', 'lecture_date']
    list_display = ('module', 'lecture_name', 'lecture_description', 'lecture_date')

class PingAdmin(admin.ModelAdmin):
    fields = ['student', 'lecture', 'ping_date']
    list_display = ('student', 'lecture', 'ping_date')

# class StatsAdmin(admin.ModelAdmin):
#     model = Stats

    # def get_urls(self):
    #     view_name = '{}_{}_changelist'.format(
    #         self.model._meta.app_label, self.model._meta.model_name)
    #     return [
    #         path('admin/stats/', self),
    #     ]

# Register your models here.
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Ping, PingAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(Stats, StatsAdmin)