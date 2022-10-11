from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.stats, name='stats'),
    path('<int:lecture_id>/students', views.students, name='student_view'),
    path('<int:module_id>', views.module, name='module'),
    path('<int:question_id>/', views.questiondetail, name='question_detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # fv - implement lecture view later
    # path('<int:lecture_id>/', views.lecture, name='lecture'),
]