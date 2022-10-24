from django.urls import path

from . import views

app_name ="tcapp"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:module_name>', views.module, name='module'),
    path('<str:module_name>/lecture/<int:lecture_id>/', views.lecture, name='lecture'),
    path('<str:module_name>/lecture/<int:lecture_id>/students', views.students, name='students'),
    path('<str:module_name>/lecture/<int:lecture_id>/submit', views.submit, name='submit'),
    path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('question/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('question/<int:question_id>/vote/', views.vote, name='vote'),
    # fv - implement stats view later
    # path('', views.stats, name='stats'),
]