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


class AbbreviatedLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
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
        return AbbreviatedLectureSerializer(lectures, many=True).data


class PingSerializer(serializers.ModelSerializer):
    # return the student username and the lecture shortname here instead of pk numbers
    student = serializers.CharField(source="student.username")
    lecture = serializers.CharField(source="lecture.lecture_shortname")

    def create(self, validated_data):
        lecture = Lecture.objects.get(
            lecture_shortname=validated_data["lecture"]["lecture_shortname"]
        )
        student = User.objects.get(username=validated_data["student"]["username"])
        return Ping.objects.create(
            lecture=lecture, student=student, ping_date=validated_data["ping_date"]
        )

    class Meta:
        model = Ping
        fields = ["ping_date", "student", "lecture"]


class ResetSerializer(serializers.ModelSerializer):
    # could do same as pings above if this information is ever needed for export or if returning usernames and lecture names is desirable in future

    class Meta:
        model = Reset
        fields = ["reset_time", "instructor", "lecture"]
