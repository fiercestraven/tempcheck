
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

class Module(models.Model):
    module_shortname = models.CharField(max_length=200, unique=True)
    module_name = models.CharField(max_length=200)
    module_description = models.TextField(default = "", blank=True)
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ForeignKey
    # protect on deletion so that deleting a user does not eliminate associated modules
    instructor = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'is_staff': True},)
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

class Reset(models.Model):
    reset_time = models.DateTimeField('date and time of reset')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

class Threshold(models.Model):
    # validators for DecimalField: https://docs.djangoproject.com/en/4.1/ref/forms/fields/
    yellow_percentage = models.DecimalField(default=15.00, max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(100.00)])
    orange_percentage = models.DecimalField(default=25.00, max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(100.00)])
    red_percentage = models.DecimalField(default=35.00, max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(100.00)])
    # only allow one set of thresholds per instructor by using OneToOneField: https://docs.djangoproject.com/en/4.1/topics/db/examples/one_to_one/
    instructor = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True},)

class User_Module(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Ping(models.Model):
    ping_date = models.DateTimeField('date and time of ping')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

# fv to do - take these out later if not using
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
