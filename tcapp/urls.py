# fv - below admin part is from tutorial https://learndjango.com/tutorials/django-login-and-logout-tutorial; not sure if needed
# from django.contrib import admin
from django.urls import path, include

from . import views

app_name ="tcapp"
urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('', views.IndexView.as_view(), name='index'),
        # fv - revisit path names below for students. Not sure what makes sense here.
    path('<str:module_name>/', views.module, name='module'),
    path('<str:module_name>/lecture/<int:lecture_id>/', views.lecture, name='lecture'),
    path('<str:module_name>/lecture/<int:lecture_id>/students/', views.students, name='students'),
    path('<str:module_name>/lecture/<int:lecture_id>/submit/', views.submit, name='submit'),
    path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('question/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('question/<int:question_id>/vote/', views.vote, name='vote'),
    # fv - implement stats view later
    # path('', views.stats, name='stats'),
]