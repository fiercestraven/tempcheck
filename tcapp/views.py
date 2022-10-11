from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the index for the temperature check app.")
    # fv - figure out how to display lectures here as dropdown or buttons or whatever

def students(request, lecture_id):
    response = "Welcome to lecture %s."
    return HttpResponse(response  % lecture_id)

# fv - it looks like anything other than index may have to take an argument... figure out how to do stats page later
# def stats(request):
#     return HttpResponse("The stats page is still under construction. Check back later!")

def module(request, module_id):
    return HttpResponse("You're looking at module %s." % module_id)
    # fv - insert list of lectures here

# fv - can't currently access lectures - need to figure out how to chain module_id/lecture_id (and how to still be able to access modules after)
# def lecture(request, lecture_id):
#     return HttpResponse("You're looking at lecture %s." % lecture_id)

def questiondetail(request, question_id):
    # shortcut version using get_object_or_404
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'tcapp/questiondetail.html', {'question': question})

def results(request, question_id):
    # dummy placeholder
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    # initial dummy response
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'tcapp/questiondetail.html', {
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
