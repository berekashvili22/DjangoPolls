from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . models import Question, Choice, Vote
from . serializers import QuestionSerializer, ChoiceSerializer, VoteSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Question List':'question-list',
        'Question Detail View':'question-detail/<str:pk>/',
        'Create Vote':'question-vote/',
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

    # 
    user = request.user
    vote = Vote.objects.filter(user=user, choice__in=choices)
    current_user_vote_status = None
    if vote:
        current_user_vote_status = 'you already voted'
    else:
        current_user_vote_status = 'you can vote'
    if question.completed == False:
        data = {
            'question': question_serializer.data,
            'choices': choices_serializer.data,
        }
    elif question.completed == True:
        choices_text = []
        votes_count = []
        for choice in choices_serializer.data:
            choice_text = choice['choice_text']
            vote_count = Vote.objects.filter(choice__id=choice['id']).count()
            choices_text.append(choice_text)
            votes_count.append(vote_count)
        
        data = {
            'question': question_serializer.data,
            'choices_text': choices_text,
            'votes_count': votes_count,
            'current_user_vote_status': current_user_vote_status,
        }

    return Response(data)

@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET'])
def questionVote(request):
    if request.method == 'GET':
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
    if request.method == 'POST':
        serializer = VoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  
    return Response(serializer.data)
 
