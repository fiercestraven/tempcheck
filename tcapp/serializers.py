from rest_framework import serializers
from .models import User, Module, Lecture, Ping, Reset

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_staff']


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        depth = 1
        fields = ['lecture_name', 'lecture_description', 'lecture_date', 'module']


class ModuleSerializer(serializers.ModelSerializer):
    # explicitly using ProfileSerializer rather than the generic User here so that only desired fields are displayed
    instructor = ProfileSerializer()
    lectures = serializers.SerializerMethodField()
    class Meta:
        model = Module
        ordering = ['module_shortname', 'lectures']
        depth = 1
        fields = ['module_shortname', 'module_name', 'module_description', 'instructor', 'is_active', 'lectures']

    def get_lectures(self, obj):
        lectures = obj.lecture_set.all().order_by('lecture_name')
        return LectureSerializer(lectures, many=True).data


class PingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ping
        fields = ['ping_date', 'student', 'lecture']
        # put in read-only fields so they're not required at POST but are still included 
        # https://www.django-rest-framework.org/api-guide/fields/
        # read_only_fields = ['ping_date', 'student', 'lecture']


class ResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reset
        fields = ['reset_time', 'lecture']
        # put in read-only field for date/time so it's not required at POST but is still included 
        # read_only_fields = ['reset_time', 'lecture']


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