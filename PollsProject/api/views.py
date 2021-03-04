from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . models import Question, Choice
from . serializers import QuestionSerializer, ChoiceSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List':'task-list',
        'Detail View':'/task-detail/<str:pk>',
        'Create':'/task-create/',
        'Update':'/task-update/<str:pk>',
        'Delete':'/task-delete/<str:pk>',
    }
    return Response(api_urls)


@api_view(['GET'])
def questionList(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def questionDetail(request, pk):
    question = Question.objects.get(pk=pk)
    choices = Choice.objects.filter(question=question)

    question_serializer = QuestionSerializer(question, many=False)
    choices_serializer = ChoiceSerializer(choices, many=True)

    data = {
        'question': question_serializer.data,
        'choices': choices_serializer.data,
    }

    return Response(data)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def questionVote(request):
    pass
 
