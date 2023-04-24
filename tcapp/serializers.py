from rest_framework import serializers
from .models import User, Module, Lecture, Ping, Reset


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "is_staff"]


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        depth = 1
        fields = [
            "lecture_shortname",
            "lecture_name",
            "lecture_description",
            "lecture_date",
            "module",
        ]


class ModuleSerializer(serializers.ModelSerializer):
    # explicitly using ProfileSerializer rather than the generic User here so that only desired fields are displayed
    instructor = ProfileSerializer()
    # adding lectures to the serialized data; empty method defaults to 'get_lectures' here: https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    lectures = serializers.SerializerMethodField()

    class Meta:
        model = Module
        ordering = ["module_shortname", "lectures"]
        depth = 1
        fields = [
            "module_shortname",
            "module_name",
            "module_description",
            "instructor",
            "is_active",
            "lectures",
        ]

    def get_lectures(self, obj):
        lectures = obj.lecture_set.all().order_by("lecture_shortname")
        return LectureSerializer(lectures, many=True).data


class PingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ping
        fields = ["ping_date", "student", "lecture"]


class ResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reset
        fields = ["reset_time", "instructor", "lecture"]
