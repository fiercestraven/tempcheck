from django.urls import path

from . import views

app_name ="tcapp"
urlpatterns = [
    path('index/', views.index, name='index'),
    path('<str:module_name>', views.module, name='module'),
    path('<str:module_name>/lecture/<int:lecture_id>/', views.lecture, name='lecture'),
    path('<str:module_name>/lecture/<int:lecture_id>/students', views.students, name='students'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('question/<int:question_id>/results/', views.results, name='results'),
    path('question/<int:question_id>/vote/', views.vote, name='vote'),
    # fv - implement stats view later
    # path('', views.stats, name='stats'),
]