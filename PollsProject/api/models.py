from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.utils.timesince import timesince


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')

    def FORMAT(self):
        return f'Created {timesince(self.pub_date)} ago'

    def __str__(self):
        return self.question_text
    
    @property
    def was_published_recently(self):
        now = timezone.localtime(timezone.now())
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @property
    def was_bulished_in_present(self):
        now = timezone.localtime(timezone.now())
        return self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'choice')
    
    def __str__(self):
        return f'{self.user} on {self.choice.question}  {self.choice}'

