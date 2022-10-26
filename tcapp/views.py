# from datetime import datetime
# from pickle import PicklingError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# from django.template import loader

from .models import Choice, Ping, Question, Lecture, Module, Student

# Create your views here.

# can omit below thanks to template view in urls
# def index(request):
#     return render(request, 'tcapp/index.html')

def students(request, module_name, lecture_id):
    module = get_object_or_404(Module, module_name=module_name)
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    return render(request, 'tcapp/students.html', {'module': module, 'lecture': lecture})

def submit(request, module_name, lecture_id):
    if request.method=="POST":
        pdate=timezone.now()
        module = get_object_or_404(Module, module_name=module_name)
        lecture = get_object_or_404(Lecture, pk=lecture_id)
        # student = get_object_or_404(Student, pk=Student.id)
        # fv - do something here to give the ping an actual student (from login info)
        pstudent = Student.objects.create(first_name="Lira", last_name="Learner", username="llearner", student_password="thinks33")
        Ping.objects.create(ping_date=pdate, student=pstudent, lecture=lecture)
        return render(request, 'tcapp/submit.html', {'module': module, 'lecture': lecture})
    else:
        return HttpResponseRedirect(reverse('tcapp:students', args=(module.module_name, lecture.id)))

# fv - it looks like anything other than index may have to take an argument... do stats page later
# def stats(request):
#     return HttpResponse("The stats page is still under construction. Check back later!")

class LecturesView(generic.ListView):
    template_name = 'tcapp/lectures.html'
    context_object_name = 'module_list'
    def get_queryset(self):
        """Return the lists of modules."""
        return Module.objects.order_by('module_name').filter(is_active = True)
# def lectures(request):
#     module_list = Module.objects.order_by('module_name')
#     lecture_list = Lecture.objects.order_by('lecture_name')
#     template = loader.get_template('tcapp/lectures.html')
#     context = {
#         'module_list': module_list,
#         'lecture_list': lecture_list,
#     }
#     return HttpResponse(template.render(context, request))

# fv - should be able to omit this view
def module_detail(request, module_name):
    return HttpResponse("You're looking at {0}.".format(module_name))
    # fv - fix this so that if there's no module by that name, it returns an error

def lecture_detail(request, module_name, lecture_id):
    return HttpResponse("You're looking at module {0}, lecture {1}.".format(module_name, lecture_id))

class QuestionView(generic.DetailView):
    model = Question
    template_name = 'tcapp/question.html'
# def question(request, question_id):
#     # shortcut version using get_object_or_404
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'tcapp/question.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'tcapp/results.html'
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'tcapp/results.html', {'question': question})

def vote(request, question_id):
    # initial dummy response
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'tcapp/question.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('tcapp:results', args=(question.id,)))
