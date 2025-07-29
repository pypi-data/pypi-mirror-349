from rest_framework import serializers
from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']

class QuestionSerializer(serializers.ModelSerializer):
    choice_set = ChoiceSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'was_published_recently', 'choice_set']