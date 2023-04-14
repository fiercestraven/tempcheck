from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Ping, Lecture, Module, Threshold, Reset, User_Module
from tcapp.serializers import (
    ModuleSerializer,
    LectureSerializer,
    PingSerializer,
    ProfileSerializer,
    ResetSerializer,
)

# Views


# fv - could remove later now that this is done through Next; leaving for ability to see Django side for now
@csrf_exempt
def api_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        return HttpResponse("Hello, " + username)


# API views #
class ProfileView(APIView):
    """
    API endpoint with profile information, used to greet and determine staff status.
    """

    def get(self, request, format=None):
        user = self.request.user
        response = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
        }
        return Response(response)

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class LectureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lectures to be viewed or edited.
    """

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # return all lectures
            return Lecture.objects.all()
        elif user.is_staff:
            # return only lectures for active modules that the instructor teaches
            return Lecture.objects.filter(module__instructor=user)
        else:
            # return lectures for active modules for which the user is enrolled
            # query constructed using shell
            return Lecture.objects.filter(module__user_module__user=user)

    lookup_field = "lecture_name"
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]


# https://www.django-rest-framework.org/api-guide/generic-views/
class ModuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows modules to be viewed or edited.
    """

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # return all modules, including inactive modules
            return Module.objects.all().order_by("module_shortname")
        elif user.is_staff:
            # return only modules that the instructor teaches
            return user.module_set.filter(is_active=True).order_by("module_shortname")
        else:
            # return active modules for which the logged-in user is enrolled
            # query constructed in the shell
            return Module.objects.filter(
                user_module__user=user, is_active=True
            ).order_by("module_shortname")

    lookup_field = "module_shortname"
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class PingView(APIView):
    """
    API endpoint that captures data from a ping submission or displays ping data for a lecture.
    """

    # https://www.codespeedy.com/django-submit-form-data-with-post-method/
    def post(self, request, lecture_name, format=None):
        student = self.request.user
        lecture = Lecture.objects.get(lecture_name=lecture_name)

        if not lecture.module.user_module_set.filter(user=student).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = PingSerializer(
            data={
                "ping_date": datetime.now(),
                "lecture": lecture.pk,
                "student": student.pk,
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, lecture_name, format=None):
        user = self.request.user
        lecture = Lecture.objects.get(lecture_name=lecture_name)
        pings = Ping.objects.filter(lecture=lecture).order_by("ping_date")
        if user.is_superuser or user.is_staff:
            return Response(PingSerializer(pings, many=True).data)
        else:
            return Response(status=HTTP_403_FORBIDDEN)

    permission_classes = [permissions.IsAuthenticated]


class ResetView(APIView):
    """
    API endpoint for capturing reset button input.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, lecture_name, format=None):
        user = self.request.user
        lecture = Lecture.objects.get(lecture_name=lecture_name)

        if user != lecture.module.instructor:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ResetSerializer(
            data={
                "reset_time": datetime.now(),
                "instructor": user.pk,
                "lecture": lecture.pk,
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LectureTemperatureView(APIView):
    """
    API endpoint for transmitting ping threshold.
    """

    def get(self, request, lecture_name, format=None):
        # count pings in the last two minutes
        lec = Lecture.objects.get(lecture_name=lecture_name)

        # set cutoff time
        cutoff = timezone.now() - timedelta(minutes=2)
        # adjust cutoff if the reset button has been pressed more recently than the cutoff time
        # handle if no resets currently associated with the lecture
        last_reset = lec.reset_set.order_by("reset_time").last()
        if last_reset is not None:
            cutoff = max(last_reset.reset_time + timedelta(minutes=2), cutoff)

        # fv - later, make sure we're only pulling distinct students here to avoid student who try to sneaky multiple ping - could do at ping creation point or here
        # count number of pings since the last cutoff
        # ping date: https://docs.python.org/3/library/datetime.html
        pcount = lec.ping_set.filter(ping_date__gt=cutoff).count()

        # get number of students enrolled in the module
        mod = lec.module
        num_students = mod.user_module_set.count()

        # get instructor and their thresholds
        try:
            thresh = mod.instructor.threshold
        except User.threshold.RelatedObjectDoesNotExist:
            # if instructor hasn't set thresholds, create ephemeral defaults
            thresh = Threshold(
                yellow_percentage=15,
                orange_percentage=25,
                red_percentage=35,
                instructor=mod.instructor,
            )

        t1 = thresh.yellow_percentage
        t2 = thresh.orange_percentage
        t3 = thresh.red_percentage

        # calculate what percentage of students have pinged in last given time frame
        percent_pings = (pcount / num_students) * 100
        if percent_pings >= t1 and percent_pings < t2:
            threshold = 1
        elif percent_pings >= t2 and percent_pings < t3:
            threshold = 2
        elif percent_pings >= t3:
            threshold = 3
        else:
            threshold = 0
        return Response(threshold)

    # allow unauthenticated requests to this particular API so the lightbulb can pull data. Only a get is defined above so no need to make read only.
    permission_classes = [permissions.AllowAny]
