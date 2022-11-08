# fv - below admin part is from tutorial https://learndjango.com/tutorials/django-login-and-logout-tutorial; not sure if needed
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views
# fv - can remove below 5 lines if not using for stats view
# from django.contrib import admin
# from adminplus.sites import AdminSitePlus

# admin.site = AdminSitePlus()
# admin.sites.site = admin.site
# admin.autodiscover()

app_name ="tcapp"
urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='tcapp/index.html'), name='index'),
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