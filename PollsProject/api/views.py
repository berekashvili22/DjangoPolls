from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from . models import Question, Choice, Vote
from . serializers import QuestionSerializer, ChoiceSerializer, VoteSerializer
from django.shortcuts import get_object_or_404

from . utils import getVoteCount, getVotesCount, getChartData


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Question List':'question-list',
        'Question Detail View':'question-detail/<str:pk>/',
        'Create Vote':'question-vote/',
        'Daily Question':'question-daily/',
    }
    return Response(api_urls)

@api_view(['GET'])
def questionOfTheDay(reqeust):
    now = timezone.localtime(timezone.now())
    question = Question.objects.filter(pub_date__lte=now).order_by('-id').first()
    serializer = QuestionSerializer(question, many=False)
    data = {
        'question': serializer.data,
        'votesCount': getVoteCount(question),
    }
    return Response(data)


class questionList(ListAPIView):
    questions = Question.objects.filter(completed=True).order_by('-pub_date')
    filtered_questions = [x for x in questions if x.was_bulished_in_present]

    queryset = filtered_questions
    serializer_class = QuestionSerializer
    pagination_class = PageNumberPagination
    
    def list(self, request, *args, **kwargs):
        response = super(questionList, self).list(request, args, kwargs)
        response.data[ 'votesCount' ] = getVotesCount(self.filtered_questions)
        return response

@api_view(['GET'])
def questionDetail(request, pk):
    # get question and question choices
    question = Question.objects.get(pk=pk)
    choices = Choice.objects.filter(question=question)
    # serialize data
    question_serializer = QuestionSerializer(question, many=False)
    choices_serializer = ChoiceSerializer(choices, many=True)
    user = request.user
    # check if user voted on currect question
    vote = Vote.objects.filter(user=user, choice__in=choices).first()
    canVote = None
    # set user vote status
    if vote:
        canVote = False
        # get choice id to check voted radio button
        userChoiceId = vote.choice.id
    else:
        canVote = True
        userChoiceId = None
    
    # check if question is completed
    if question.completed == True:
        canVote = False;

    # get data for chart
    choices = choices_serializer.data
    chartData = getChartData(choices)


    # create data for front
    data = {
        'question': question_serializer.data,
        'choices': choices_serializer.data,
        'canVote': canVote,
        'userChoiceId': userChoiceId,
        'chartData': chartData,
        'total_votes': getVoteCount(question),
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
 
