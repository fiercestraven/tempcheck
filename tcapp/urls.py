# fv - below admin part is from tutorial https://learndjango.com/tutorials/django-login-and-logout-tutorial; not sure if needed
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers

# api endpoints - generic api views (as opposed to ModelViewSets) are listed below in the urlpatterns
router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# on using 'basename' below to quiet to an error due to no queryset in the View: https://www.django-rest-framework.org/api-guide/routers/
router.register(r'modules', views.ModuleViewSet, basename='modules')
router.register(r'lectures', views.LectureViewSet)
router.register(r'pings', views.AllPingViewSet)


app_name ="tcapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.views.LoginView
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.api_login, name='api_login'),
    path('lectures/', views.LecturesView.as_view(), name='lectures'),
    path('lectures/<str:module_shortname>/<str:lecture_name>/', views.lecture_detail, name='lecture_detail'),
    path('lectures/<str:module_shortname>/<str:lecture_name>/submit/', views.submit, name='submit'),
    # path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
    # path('question/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('question/<int:question_id>/vote/', views.vote, name='vote'),
    path('stats/', TemplateView.as_view(template_name='tcapp/stats.html'), name='stats'),
    path('api/', include(router.urls)),
    # can't add a generic view in a router, so these api views are here instead of above
    path('api/lectures/<str:lecture_name>/temperature/', views.LectureTemperatureView.as_view(), name='temperature'),
    path('api/lectures/<str:lecture_name>/resets/', views.ResetView.as_view(), name='resets'),
    path('api/lectures/<str:lecture_name>/pings/', views.PingView.as_view(), name='pings'),
    path('api/profile/', views.ProfileView.as_view(), name='profile'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]