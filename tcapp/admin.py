from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.urls import path, reverse
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from .models import Module, Lecture, Ping, User, User_Module, Threshold, Reset
from rest_framework.authtoken.models import TokenProxy
from django.utils.translation import gettext_lazy as _


# set basic permissions for is_staff users (delete is added in each class where required)
# https://docs.djangoproject.com/en/4.1/topics/auth/default/#topic-authorization
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
    # hide fields for groups and user permissions for everyone - modify fieldsets from Django's UserAdmin
    # Display options: https://stackoverflow.com/questions/60165306/django-admin-exclude-in-useradmin
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = [
        (
            "Account info",
            {"fields": ["username", "password1", "password2", "is_staff"]},
        ),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
    ]
    list_filter = ("is_staff",)
    list_display = ("username", "first_name", "last_name", "email", "is_staff")

    # instructors have view and add permissions, along with some change permissions, but not delete
    # set up permissions so that only a superuser can assign a user as staff or a superuser
    # https://stackoverflow.com/questions/20398362/field-level-permission-django
    # https://stackoverflow.com/questions/60165306/django-admin-exclude-in-useradmin
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ("is_staff", "is_superuser", "last_login", "date_joined")
        # fix for 'NoneType' error: https://books.agiliq.com/projects/django-admin-cookbook/en/latest/uneditable_existing.html
        if obj:
            return []

    def has_delete_permission(self, request, obj=None):
        # only a superuser can do any deletion
        return request.user.is_superuser

    # defining url path for csv upload: https://www.youtube.com/watch?v=BLxCnD5-Uvc
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):
        messages.info(
            request,
            "The CSV file should adhere to the following format: username,first_name,last_name,email,is_staff",
        )
        if request.method == "POST":
            # below csv_upload is from the csvImportForm function above
            csv_file = request.FILES["csv_upload"]
            if not csv_file.name.endswith(".csv"):
                messages.warning(request, "The wrong file type was uploaded.")
                return HttpResponseRedirect(request.path_info)
            # rows = TextIOWrapper(csv_file, encoding="utf-8", newline="")
            # fix end of line \r and end of file errors
            file_data = csv_file.read().decode("utf-8").replace("\r", "").strip()
            # split into list of lines
            csv_data = file_data.split("\n")
            # iterate over lines and split into fields

            row_count = 0
            # form_errors = []
            for x in csv_data:
                row_count += 1
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
                    username=fields[0],
                    first_name=fields[1],
                    last_name=fields[2],
                    email=fields[3],
                    is_staff=fields[4],
                )
            # reverse function: https://stackoverflow.com/questions/56711082/reverse-django-admin-urls
            url = reverse("admin:auth_user_changelist")
            return HttpResponseRedirect(url)
        form = csvImportForm
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


class ModuleAdmin(StaffPermission, admin.ModelAdmin):
    fields = [
        "module_shortname",
        "module_name",
        "module_description",
        "instructor",
        "is_active",
    ]
    list_filter = ("is_active",)
    list_display = (
        "module_shortname",
        "module_name",
        "module_description",
        "instructor",
        "is_active",
    )

    # let instructors change or delete only their own modules
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # if no obj given, only show change options if user is staff
        if obj is None:
            return request.user.is_staff
        # if user is the instructor for this module, allow changes
        else:
            return request.user == obj.instructor

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        # if user is the instructor for this module, allow delete
        else:
            return request.user == obj.instructor


class User_ModuleAdmin(StaffPermission, admin.ModelAdmin):
    fields = ["module", "user"]
    list_filter = ("module",)
    list_display = ("module", "user")

    # let instructors change and delete student-module objects only from modules that they teach
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.module.instructor

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.module.instructor


class LectureAdmin(StaffPermission, admin.ModelAdmin):
    fields = ["module", "lecture_shortname", "lecture_description", "lecture_date"]
    list_display = (
        "module",
        "lecture_shortname",
        "lecture_description",
        "lecture_date",
    )

    # let instructors change and delete only lectures that are part of modules that they teach
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.module.instructor

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.module.instructor


class ResetAdmin(StaffPermission, admin.ModelAdmin):
    fields = ["reset_time", "lecture"]
    list_display = ("reset_time", "lecture")

    # only admin users can add resets
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

    # let instructors view, change and delete only resets that are part of lectures that they teach
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.lecture.module.instructor

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.lecture.module.instructor

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.lecture.module.instructor


class ThresholdAdmin(StaffPermission, admin.ModelAdmin):
    fields = ["instructor", "yellow_percentage", "orange_percentage", "red_percentage"]
    list_display = (
        "instructor",
        "yellow_percentage",
        "orange_percentage",
        "red_percentage",
    )

    # let instructors change and delete only their own thresholds
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.instructor

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.instructor


# instructors can only view pings and do not have add, change, or delete access to pings. This is reserved for the superuser.
class PingAdmin(admin.ModelAdmin):
    fields = ["student", "lecture", "ping_date"]
    list_display = ("student", "lecture", "ping_date")

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        else:
            return request.user == obj.lecture.module.instructor


# Register models
# unregister default User model before adding custom model: https://stackoverflow.com/questions/2552516/changing-user-modeladmin-for-django-admin#255%202554
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(User_Module, User_ModuleAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Reset, ResetAdmin)
admin.site.register(Threshold, ThresholdAdmin)
admin.site.register(Ping, PingAdmin)

# remove auth token from admin display (https://stackoverflow.com/questions/51710455/hide-the-token-table-from-the-admin-panel-in-django-rest-framework)
admin.site.unregister(TokenProxy)
