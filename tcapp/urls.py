# fv - below admin part is from tutorial https://learndjango.com/tutorials/django-login-and-logout-tutorial; not sure if needed
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views
from django.contrib.auth import views as auth_views

app_name ="tcapp"
urlpatterns = [
    path('', views.index, name='index'),
    # https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.views.LoginView
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('signup/', views.signup, name='signup'),
    # fv - revisit module detail view - keep?
    # path('<str:module_name>/', views.module_detail, name='module_detail'),
    path('lectures/', views.LecturesView.as_view(), name='lectures'),
    path('lectures/<str:module_name>/<str:lecture_name>/', views.lecture_detail, name='lecture_detail'),
    path('lectures/<str:module_name>/<str:lecture_name>/submit/', views.submit, name='submit'),
    path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('question/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('question/<int:question_id>/vote/', views.vote, name='vote'),
    path('stats/', TemplateView.as_view(template_name='tcapp/stats.html'), name='stats'),
]