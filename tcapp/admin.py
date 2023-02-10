from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.urls import path, reverse
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from .models import Module, Lecture, Ping, User, Student_Module, Threshold
from rest_framework.authtoken.models import TokenProxy

# set basic permissions for is_staff users (delete is added in each class where required)
class StaffPermission(object):
    def has_module_permission(self, request):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff



class csvImportForm(forms.Form):
    csv_upload = forms.FileField()

class UserAdmin(StaffPermission, UserAdmin):
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
        messages.info(request, "The CSV file should adhere to the following format: username,first_name,last_name,email,is_staff")
        if request.method == "POST":
            # below csv_upload is from the csvImportForm function above
            csv_file = request.FILES["csv_upload"]
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded.')
                return HttpResponseRedirect(request.path_info)
            # rows = TextIOWrapper(csv_file, encoding="utf-8", newline="")
            # fix end of line \r and end of file errors
            file_data = csv_file.read().decode("utf-8").replace('\r', '').strip()
            # split into list of lines
            csv_data = file_data.split("\n")
            # iterate over lines and split into fields
            
            row_count = 0
            # form_errors = []
            for x in csv_data:
                row_count +=1
                # fv - note: here, put into a form and then run validation - if working, can delete from fields=x.split(",")
                # fv - could try following this: https://djangosource.com/django-csv-upload.html
                # form = csvImportForm(x)
                # if not form.is_valid():
                #     form_errors = form.errors
                #     break
                # form.save()
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

class ModuleAdmin(StaffPermission, admin.ModelAdmin):
    fields = ['module_shortname', 'module_name', 'module_description', 'instructor', 'is_active']
    list_filter = ('is_active',)
    list_display = ('module_shortname', 'module_name', 'module_description', 'instructor', 'is_active')

    # let instructors change or delete only their own modules
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.instructor

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.instructor
        

class Student_ModuleAdmin(StaffPermission, admin.ModelAdmin):
    fields = ['module', 'student']
    list_filter = ('module',)
    list_display = ('module', 'student')

    # let instructors change and delete student-module objects only from modules that they teach
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.module.instructor
    
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.module.instructor

class LectureAdmin(StaffPermission, admin.ModelAdmin):
    fields = ['module', 'lecture_name', 'lecture_description', 'lecture_date']
    list_display = ('module', 'lecture_name', 'lecture_description', 'lecture_date')

    # let instructors change and delete only lectures that are part of modules that they teach
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.module.instructor
    
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.module.instructor
    
    

class ThresholdAdmin(StaffPermission, admin.ModelAdmin):
    fields = ['instructor', 'yellow_percentage', 'orange_percentage', 'red_percentage']
    list_display= ('instructor', 'yellow_percentage', 'orange_percentage', 'red_percentage')

    # let instructors change and delete only their own thresholds
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.instructor
    
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.instructor

# instructors do not have add, change, or delete access to pings. This is reserved for the admin user.
class PingAdmin(admin.ModelAdmin):
    fields = ['student', 'lecture', 'ping_date']
    list_display = ('student', 'lecture', 'ping_date')

# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#         (None,               {'fields': ['lecture']}),
#     ]
#     inlines = [ChoiceInline]
#     list_display = ('question_text', 'lecture', 'pub_date')

# class StatsAdmin(admin.ModelAdmin):
#     model = Stats

    # def get_urls(self):
    #     view_name = '{}_{}_changelist'.format(
    #         self.model._meta.app_label, self.model._meta.model_name)
    #     return [
    #         path('admin/stats/', self),
    #     ]

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Student_Module, Student_ModuleAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Threshold, ThresholdAdmin)
admin.site.register(Ping, PingAdmin)
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Stats, StatsAdmin)

# remove auth token from admin display (https://stackoverflow.com/questions/51710455/hide-the-token-table-from-the-admin-panel-in-django-rest-framework)
admin.site.unregister(TokenProxy)