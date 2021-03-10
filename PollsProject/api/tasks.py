from . models import Question
from django.utils import timezone

def update_poll_status():
    # find polls that created 12 hour ago and set them completed status to True

    # test for less time
    twelve_hour_ago = timezone.now() - timezone.timedelta(hours=12)
    completed_questions = Question.objects.filter(
        pub_date__lte=twelve_hour_ago
    )
    if completed_questions:
        for question in completed_questions:
            question.completed = True
            question.save()
    else:
        return True
