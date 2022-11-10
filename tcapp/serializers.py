from rest_framework import serializers
from . models import User, Module, Lecture, Student_Module, Ping, Question, Choice
  
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'module_name', 'module_description', 'instructor', 'is_active']

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'lecture_name', 'lecture_description', 'lecture_date', 'module']

# class Student_ModuleSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
    # fv - figure out how to base this one on two models...
        # model = Module, User
        # fields = ['id', 'module', 'student']

class PingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ping
        fields = ['id', 'ping_date', 'student', 'lecture']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'lecture']

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes', 'question']