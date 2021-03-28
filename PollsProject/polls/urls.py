from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('today/', views.poll, name='today'),
    path('polls/', views.polls, name='polls'),
    path('poll/<pk>/', views.pollDetail, name='poll-detail'),
    path('profile/', views.profile, name='profile'),
    url(r'^password/$', views.change_password, name='change_password'),
]
