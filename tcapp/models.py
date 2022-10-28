import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.

# User class tracks both students and instructors. Attribute is_staff allows users to have admin access. 
# fv - see if I can subclass Instructor and Student users... have two user types. OR look into super admin and what that can do. 
# There already is an is_staff and is_superuser - may be fine. Type something up for report.

# class Instructor(models.Model):
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     username = models.CharField(max_length=200)
#     # fv - figure out how to add security here
#     instructor_password = models.CharField(max_length=200)
#     def __str__(self):
#         return self.username

class Module(models.Model):
    module_name = models.CharField(max_length=200)
    module_description = models.TextField(default = "")
    # fv - look and see if there's a way to restrict the User below to only accept is_staff options. Justify decision either way.
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.module_name

class Lecture(models.Model):
    lecture_name = models.CharField(max_length=200)
    lecture_description = models.TextField(default = "")
    lecture_date = models.DateTimeField('date of lecture')
    # insert foreign key to module_id
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    def __str__(self):
        return self.lecture_name

# fv - nix this and use Django built in User model? ADD EMAIL
# class Student(models.Model):
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     username = models.CharField(max_length=200)
#     # fv - figure out how to add security here
#     student_password = models.CharField(max_length=200)
#     def __str__(self):
#         return self.username

class Student_Module(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

# class Student_Lecture(models.Model):
#     lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Ping(models.Model):
    ping_date = models.DateTimeField('date and time of ping')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    # fv - come up with something useable here?
    # def __str__(self):
    #     return 

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    def __str__(self):
        return self.question_text
    @admin.display(
        boolean=True,
        ordering='-pub_date',
        description='Publication Date',
    )
    def is_published(self, obj):
        return Question.pub_date is not None

class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return self.choice_text
