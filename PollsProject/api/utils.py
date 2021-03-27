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

def getChartData(choices):
    choices_text = []
    votes_count = []

    # loop through choices
    for choice in choices:
            # get choice text for each choice
            choice_text = choice['choice_text']
            # get vote count for each choice
            vote_count = Vote.objects.filter(choice__id=choice['id']).count()

            # add choice data to lists
            choices_text.append(choice_text)
            votes_count.append(vote_count)
    
    data = {
        'text': choices_text,
        'count': votes_count,
    }

    return data
    