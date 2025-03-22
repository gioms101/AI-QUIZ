from rest_framework import serializers
from .models import Question


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
