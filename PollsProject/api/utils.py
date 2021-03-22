from . models import Question, Choice, Vote

def getVoteCount(question):
    choices = Choice.objects.filter(question=question)
    voteCount = Vote.objects.filter(choice__in=choices).count()
    return voteCount

def getVotesCount(questions):
    voteCounts = {}
    for question in questions:
        questionId = question.id
        count = getVoteCount(question)
        voteCounts.update({questionId: count})
    return voteCounts