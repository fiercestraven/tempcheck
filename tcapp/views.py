from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request, lecture):
    return HttpResponse("Hello, world. You're at the index for the temperature check app.")
    # fv - figure out how to display lectures here as dropdown or buttons or whatever

def students(request, lecture_id):
    response = "Welcome to lecture %s."
    return HttpResponse(response  % lecture_id)

def stats(request):
    return HttpResponse("The stats page is still under construction. Check back later!")

def lecture(request, lecture_id):
    return HttpResponse("You're looking at lecture %s." % lecture_id)