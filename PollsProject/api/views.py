from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone


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
def questionOfTheDay(reqeust):
    now = timezone.localtime(timezone.now())
    question = Question.objects.filter(pub_date__lte=now).order_by('-id').first()
    serializer = QuestionSerializer(question, many=False)
    # get votes count
    choices = Choice.objects.filter(question=question)
    votesCount = Vote.objects.filter(choice__in=choices).count()

    data = {
        'question': serializer.data,
        'votesCount': votesCount,
    }
    return Response(data)


@api_view(['GET'])
def questionList(request):
    questions = Question.objects.filter(completed=True).order_by('-pub_date')
    filtered_questions = [x for x in questions if x.was_bulished_in_present]
    serializer = QuestionSerializer(filtered_questions, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def questionDetail(request, pk):
    # get question and question choices
    question = Question.objects.get(pk=pk)

    choices = Choice.objects.filter(question=question)

    # serialize data
    question_serializer = QuestionSerializer(question, many=False)
    choices_serializer = ChoiceSerializer(choices, many=True)

    # get reqeust user
    user = request.user

    # check if user voted on currect question
    vote = Vote.objects.filter(user=user, choice__in=choices).first()
    canVote = None
    # if vote exists that means user has already on that question so set canVote to false
    if vote:
        canVote = False
        # get choice id to check voted radio button
        userChoiceId = vote.choice.id
    # else set canVote to true
    else:
        canVote = True
        userChoiceId = None
    
    # check if question is completed if not , if its complted set canVote to false  
    if question.completed == True:
        canVote = False;

    # ------------------------
    #      this data will be user for data visualization (with zingcharts)

    # create empty lists for choice data
    choices_text = []
    votes_count = []

    # loop through currenct question choices
    for choice in choices_serializer.data:
            # get choice text for each choice
            choice_text = choice['choice_text']
            # get vote count for each choice
            vote_count = Vote.objects.filter(choice__id=choice['id']).count()

            # add choice data to lists
            choices_text.append(choice_text)
            votes_count.append(vote_count)

    # ------------------------

    # create data for front
    data = {
        'question': question_serializer.data,
        'choices': choices_serializer.data,
        'canVote': canVote,
        'userChoiceId': userChoiceId,
        'choices_text': choices_text,
        'votes_count': votes_count,
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
 
