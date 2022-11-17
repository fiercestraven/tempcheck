from rest_framework import serializers
from .models import User, Module, Lecture, Student_Module, Ping, Question, Choice
  
# for hyperlinking: https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'module_name', 'module_description', 'instructor', 'is_active']

class LectureSerializer(serializers.ModelSerializer):
    # module = serializers.HyperlinkedIdentityField(view_name='module', format='html')
    # module = serializers.HyperlinkedRelatedField(many=True, view_name='modules', read_only=True)

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

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='accounts',
    #     lookup_field='slug'
    # )
    # users = serializers.HyperlinkedRelatedField(
    #     view_name='user-detail',
    #     lookup_field='username',
    #     many=True,
    #     read_only=True
    # )
    url = serializers.HyperlinkedIdentityField(
        view_name='questions',
        lookup_field='id'
    )

    lecture = serializers.HyperlinkedRelatedField(
        view_name='lectures',
        lookup_field='id',
        many=True,
        read_only=True
    )

    class Meta:
        model = Question
        fields = ['url', 'id', 'question_text', 'pub_date', 'lecture']

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes', 'question']