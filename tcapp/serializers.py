from rest_framework import serializers
from .models import User, Module, Lecture, Student_Module, Ping, Question, Choice
  
# for hyperlinking: https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        depth = 1
        fields = ['lecture_name', 'lecture_description', 'lecture_date', 'module']
        # extra_kwargs = {
        #     'url': {'view_name': 'tcapp:lecture-detail', 'lookup_field': 'lecture_name'},
        #     'module': {'view_name': 'tcapp:module-detail', 'lookup_field': 'module_name'},
        # }

class ModuleSerializer(serializers.ModelSerializer):
    # explicitly using UserSerializer here so that only desired fields are displayed
    instructor = UserSerializer()
    lectures = serializers.SerializerMethodField()
    class Meta:
        model = Module
        ordering = ['module_shortname', 'lectures']
        depth = 1
        fields = ['module_shortname', 'module_name', 'module_description', 'instructor', 'is_active', 'lectures']

    def get_lectures(self, obj):
        lectures = obj.lecture_set.all().order_by('lecture_name')
        return LectureSerializer(lectures, many=True).data


# class SomeOtherThingSerializer(serializers.ModelSerializer):
#     user = UserSerializer()  # Declare this field explicitly.
#     class Meta:
#         model = SomeOtherThing
#         depth = 1

class Student_ModuleSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    class Meta:
            model = Student_Module
            depth = 1
            fields = ['module', 'student']

class PingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ping
        fields = ['id','ping_date', 'student', 'lecture']
        # put in read-only fields so they're not required at POST but are still included 
        # https://www.django-rest-framework.org/api-guide/fields/
        read_only_fields = ['ping_date', 'lecture', 'student']
        # extra_kwargs = {
        #     'url': {'view_name': 'tcapp:ping-detail'},
        #     'student': {'view_name': 'tcapp:user-detail'},
        #     'lecture': {'view_name': 'tcapp:lecture-detail'},
        # }

# class QuestionSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['url', 'id', 'question_text', 'pub_date', 'lecture']
#         extra_kwargs = {
#             'url': {'view_name': 'tcapp:question-detail'},
#             'lecture': {'view_name': 'tcapp:lecture-detail'},
#         }

# class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Choice
#         fields = ['url', 'id', 'choice_text', 'votes', 'question']
#         extra_kwargs = {
#             'url': {'view_name': 'tcapp:choice-detail'},
#             'question': {'view_name': 'tcapp:question-detail'},
#         }