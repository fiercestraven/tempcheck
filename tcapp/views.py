from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import loader

from .models import Choice, Question, Lecture, Module

# Create your views here.

def index(request):
    module_list = Module.objects.order_by('module_name')
    lecture_list = Lecture.objects.order_by('lecture_name')
    template = loader.get_template('tcapp/index.html')
    context = {
        'module_list': module_list,
        'lecture_list': lecture_list,
    }
    return HttpResponse(template.render(context, request))

def students(request, module_name, lecture_id):
    module = get_object_or_404(Module, module_name=module_name)
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    return render(request, 'tcapp/students.html', {'module': module, 'lecture': lecture})

# fv - it looks like anything other than index may have to take an argument... do stats page later
# def stats(request):
#     return HttpResponse("The stats page is still under construction. Check back later!")

def module(request, module_name):
    return HttpResponse(request, "You're looking at module {0}.".format(module_name))
    # fv - insert list of lectures here
    # fv - fix this so that if there's no module by that name, it returns an error

def lecture(request, module_name, lecture_id):
    return HttpResponse(request, "You're looking at module {0}, lecture {1}.".format(module_name, lecture_id))

def question(request, question_id):
    # shortcut version using get_object_or_404
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'tcapp/question.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'tcapp/results.html', {'question': question})

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
