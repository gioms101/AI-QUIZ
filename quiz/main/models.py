from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Question(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')


class PossibleAnswer(models.Model):
    name = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name="possible_answers")


class Answer(models.Model):
    name = models.CharField(max_length=300)  # User Answer
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")


class QuizTopic(models.Model):
    """
    This is used to count Which Quiz Topic is most generated and provide leaderboard of popular quiz topics.
    """

    name = models.CharField(max_length=150)
    asked = models.PositiveIntegerField(default=1)
