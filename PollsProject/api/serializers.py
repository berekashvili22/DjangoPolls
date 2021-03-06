# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . models import Question, Choice, Vote


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('__all__')
        optional_fields = ['user',]
        validators = []
    
    def save(self):
        user = self.context['request'].user
        choice = self.validated_data['choice']

        vote = Vote.objects.create(
            user=user,
            choice=choice
        ).save()
        return vote

        