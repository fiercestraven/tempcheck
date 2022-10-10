from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:lecture_id>/students', views.students, name='studentview'),
    path('', views.stats, name='stats'),
    path('<int:lecture_id>/', views.lecture, name='lecture'),
]