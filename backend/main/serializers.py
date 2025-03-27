from rest_framework import serializers
from .models import Question, Answer, QuizTopic


class GenerateQuizSerializer(serializers.Serializer):
    prompt = serializers.CharField()


class RetrieveQuestionSerializer(serializers.ModelSerializer):
    possible_answers = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Question
        fields = ("name", "possible_answers")


class SaveAnswerSerializer(serializers.ModelSerializer):
    user_answer = serializers.CharField(source='name')

    class Meta:
        model = Answer
        fields = ('user_answer', 'question')


class PopularQuizTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizTopic
        fields = ("name",)
