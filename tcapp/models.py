import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.

class Instructor(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    # fv - figure out how to add security here
    instructor_password = models.CharField(max_length=200)
    def __str__(self):
        return self.username

class Module(models.Model):
    module_name = models.CharField(max_length=200)
    module_description = models.TextField(default = "")
    # insert foreign key to instructor_id
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
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

class Student(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    # fv - figure out how to add security here
    student_password = models.CharField(max_length=200)
    def __str__(self):
        return self.username

class Student_Module(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Student_Lecture(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Ping(models.Model):
    ping_date = models.DateTimeField('date and time of ping')
    # create foreign keys to both student_id and lecture_id
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    # fv - come up with something useable here?
    # def __str__(self):
    #     return 

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
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
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    def __str__(self):
        return self.choice_text
