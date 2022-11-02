from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# from django.template import loader
from .forms import SignUpForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import Choice, Ping, Question, Lecture, Module

# Views

# can omit below thanks to template view in urls
# def index(request):
#     return render(request, 'tcapp/index.html')

def signup(request): 
    if request.user.is_authenticated:
        return redirect('tcapp:lectures')

    if request.method == 'POST':  
        form = SignUpForm(request.POST)  
        if form.is_valid():  
            user = form.save()  
            user.refresh_from_db()
            # fv - if I get profile stuff to work, change the 3 lines below to match: user.profile.first_name = form.cleaned_data.get('first_name')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            # fv - add message to the login page here to show it was a successful signup
            # fv - is below line working?
            return redirect('tcapp/lectures') 
        else:
            return render(request,'tcapp/signup.html',{'form':form})
    else:  
        form = SignUpForm()  
        return render(request, 'tcapp/signup.html', {'form':form})  

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('tcapp:lectures'))
        # return redirect('tcapp/lectures')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)

        if user is not None:
            login(request, user)
            return redirect('tcapp/lectures')
        else:
            form = AuthenticationForm()
            return render(request,'tcapp:login',{'form':form})
    else:
        form = AuthenticationForm()
        return render(request, 'tcapp:login', {'form':form})

@login_required
def submit(request, module_name, lecture_name):
    if request.method=="POST":
        pdate=timezone.now()
        module = get_object_or_404(Module, module_name=module_name)
        lecture = get_object_or_404(Lecture, lecture_name=lecture_name)
        student = request.user
        # pstudent = Student.objects.create(first_name="Lira", last_name="Learner", username="llearner", student_password="thinks33")
        Ping.objects.create(ping_date=pdate, student=student, lecture=lecture)
        return render(request, 'tcapp/submit.html', {'module': module, 'lecture': lecture})
    else:
        return HttpResponseRedirect(reverse('tcapp:lectures', args=(module.module_name, lecture.lecture_name)))

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
# def module_detail(request, module_name):
#     return HttpResponse("You're looking at {0}.".format(module_name))
    # fv - fix this so that if there's no module by that name, it returns an error

def lecture_detail(request, module_name, lecture_name):
    module = get_object_or_404(Module, module_name=module_name)
    lecture = get_object_or_404(Lecture, lecture_name=lecture_name)
    return render(request, 'tcapp/lecture.html', {'module': module, 'lecture': lecture})

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
