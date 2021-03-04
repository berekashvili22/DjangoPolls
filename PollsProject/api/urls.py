from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('question-list/', views.questionList, name='question-list'),
    path('question-detail/<str:pk>/', views.questionDetail, name='question-detail'),
    path('question-vote/', views.questionVote, name='question-vote'),
]
