# fv - below admin part is from tutorial https://learndjango.com/tutorials/django-login-and-logout-tutorial; not sure if needed
# from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views

app_name ="tcapp"
urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='tcapp/index.html'), name='index'),
    path('lectures/', views.LecturesView.as_view(), name='lectures'),
    # fv - revisit path names below for students. Not sure what makes sense here.
    path('<str:module_name>/', views.module_detail, name='module_detail'),
    path('<str:module_name>/lecture/<int:lecture_id>/', views.lecture_detail, name='lecture_detail'),
    # path('<str:module_name>/lecture/<int:lecture_id>/students/', views.students, name='students'),
    path('<str:module_name>/lecture/<int:lecture_id>/submit/', views.submit, name='submit'),
    path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('question/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('question/<int:question_id>/vote/', views.vote, name='vote'),
    # fv - implement stats view later
    # path('', views.stats, name='stats'),
]