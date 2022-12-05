
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# User class tracks both students and instructors. Attribute is_staff allows users to have admin access. 
# fv - see if I can subclass Instructor and Student users... have two user types. OR look into super admin and what that can do. 
# There already is an is_staff and is_superuser - may be fine. Type something up for report.

# fv - maybe implement profile later. https://dev.to/thepylot/create-advanced-user-sign-up-view-in-django-step-by-step-k9m Problem it caused was that admin login no longer worked-- said that user had no profile.
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(max_length=150)
#     # bio = models.TextField()
#     def __str__(self):
#         return self.user.username
    
# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()

class Module(models.Model):
    # module_shortname = models.CharField(max_length=200, default = "", unique=True)
    module_name = models.CharField(max_length=200, unique=True)
    module_description = models.TextField(default = "", blank=True)
    # fv - look and see if there's a way to restrict the User below to only accept is_staff options. Justify decision either way.
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.module_name

class Lecture(models.Model):
    lecture_name = models.CharField(max_length=200, unique=True)
    lecture_description = models.TextField(default = "", blank=True)
    lecture_date = models.DateField('date of lecture', blank=True)
    # insert foreign key to module_id
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    def __str__(self):
        return self.lecture_name

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
