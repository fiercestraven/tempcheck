from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Ping, Lecture, Module, Threshold
from tcapp.serializers import UserSerializer, ModuleSerializer, LectureSerializer, PingSerializer, Student_ModuleSerializer

# Views

# fv - below is part of 8 Jan trial to get the csv uploader working. These weren't helping, so I commented them out.
# def csv_upload(request):
#     return render(request, 'admin/csv_upload.html',)

# def stats(request):
#     return render(request, 'admin/stats.html',)

# fv - could remove later now that this is done through Next; leaving for ability to see Django side for now
def index(request):
    if request.user.is_authenticated:
        return redirect('tcapp:lectures')
    else:
        return render(request, 'tcapp/index.html',)

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        return HttpResponse("Hello, " + username)

# def login(request):
#     if request.user.is_authenticated:
#         return redirect('tcapp/lectures')

#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username = username, password = password)

#         if user is not None:
#             login(request, user)
#             return redirect('tcapp/lectures')
#         else:
#             form = AuthenticationForm()
#             return render(request,'tcapp:login',{'form':form})
#     else:
#         form = AuthenticationForm()
#         return render(request, 'tcapp:login', {'form':form})

@login_required
def submit(request, module_name, lecture_name):
    pdate=timezone.now()
    module = get_object_or_404(Module, module_name=module_name)
    lecture = get_object_or_404(Lecture, lecture_name=lecture_name)
    student = request.user
    if request.method=="POST":
        Ping.objects.create(ping_date=pdate, student=student, lecture=lecture)
        return render(request, 'tcapp/submit.html', {'module': module, 'lecture': lecture})
    else:
        # fv - is this working?
        return HttpResponseRedirect(reverse('tcapp:lecture_detail', args=(module.module_name, lecture.lecture_name)))

class LecturesView(generic.ListView):
    template_name = 'tcapp/lectures.html'
    context_object_name = 'module_list'
    def get_queryset(self):
        """Return the lists of modules."""
        return Module.objects.order_by('module_name').filter(is_active = True)

def lecture_detail(request, module_name, lecture_name):
    module = get_object_or_404(Module, module_name=module_name)
    lecture = get_object_or_404(Lecture, lecture_name=lecture_name)
    return render(request, 'tcapp/lecture.html', {'module': module, 'lecture': lecture})

# class QuestionView(generic.DetailView):
#     model = Question
#     template_name = 'tcapp/question.html'

# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'tcapp/results.html'

# def vote(request, question_id):
#     # initial dummy response
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'tcapp/question.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('tcapp:results', args=(question.id,)))


# API views #
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ModuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows modules to be viewed or edited.
    """
    queryset = Module.objects.all().order_by('module_shortname')
    serializer_class = ModuleSerializer
    lookup_field = 'module_shortname'
    permission_classes = [permissions.IsAuthenticated]

class LectureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lectures to be viewed or edited.
    """
    queryset = Lecture.objects.all().order_by('lecture_name')
    serializer_class = LectureSerializer
    lookup_field = 'lecture_name'
    permission_classes = [permissions.IsAuthenticated]

# https://www.django-rest-framework.org/api-guide/generic-views/
class StudentModuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows student_modules to be viewed or edited.
    """
    def get_queryset(self):
        student =self.request.user
        # return active modules for which the logged-in user is enrolled
        return student.student_module_set.all().filter(module__is_active=True).order_by('module__module_shortname')
    serializer_class = Student_ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

class PingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pings to be viewed or edited.
    """
    queryset = Ping.objects.all().order_by('ping_date')
    serializer_class = PingSerializer
    #permission_classes = [permissions.IsAuthenticated]
    # on saving/deleting hooks: https://stackoverflow.com/questions/35990589/django-rest-framework-setting-default-primarykeyrelated-field-value/35990729#35990729
    def perform_create(self, serializer):
        student = self.request.user
        # fv - figure out how to get lecture name from url instead 
        lecture = Lecture.objects.get(lecture_name=self.request.data['lecture_name'])
        serializer.save(ping_date=datetime.now(), lecture=lecture, student=student)
    def perform_update(self, serializer):
        student = self.request.user
        lecture = Lecture.objects.get(lecture_name=self.request.data['lecture_name'])
        serializer.save(ping_date=datetime.now(), lecture=lecture, student=student)
    permission_classes = [permissions.IsAuthenticated]

# class InstructorThresholdView(APIView):
#     """
#     API endpoint for transmitting instructor thresholds (and maybe also they could set the ping gray-out duration?).
#     """

#     permission_classes = [permissions.IsAuthenticated]

class LectureTemperatureView(APIView):
    """
    API endpoint for transmitting ping threshold.
    """
    def get(self, request, lecture_name, format=None):
        # count pings in the last two minutes
        lec = Lecture.objects.get(lecture_name=lecture_name)
        # fv - later, make sure we're only pulling distinct students here to avoid student who try to sneaky multiple ping - could do at ping creation point or here
        pcount = lec.ping_set.filter(ping_date__gt=(timezone.now() - timedelta(minutes=2))).count()

        # get number of students enrolled in the module
        mod = lec.module
        num_students = mod.student_module_set.count()

        # get instructor and their thresholds
        try:
            thresh = mod.instructor.threshold
        except User.threshold.RelatedObjectDoesNotExist:
            # if instructor hasn't set thresholds, create ephemeral defaults
            thresh = Threshold(yellow_percentage=15, orange_percentage=25, red_percentage=35, instructor=mod.instructor)

        t1 = thresh.yellow_percentage
        t2 = thresh.orange_percentage
        t3 = thresh.red_percentage

        # fv - take out if not using. check if instructor has pinged

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
    permission_classes = [permissions.IsAuthenticated]

# class QuestionViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows questions to be viewed or edited.
#     """
#     queryset = Question.objects.select_related('lecture').all().order_by('lecture__lecture_name')
#     serializer_class = QuestionSerializer
#     #permission_classes = [permissions.IsAuthenticated]

# class ChoiceViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows question choices to be viewed or edited.
#     """
#     queryset = Choice.objects.select_related('question').all().order_by('question__question_text')
#     serializer_class = ChoiceSerializer
#     #permission_classes = [permissions.IsAuthenticated]