from django.contrib import admin
from .models import Instructor, Module, Lecture, Student, Ping

# Register your models here.
admin.site.register(Instructor)
admin.site.register(Module)
admin.site.register(Lecture)
admin.site.register(Student)
admin.site.register(Ping)