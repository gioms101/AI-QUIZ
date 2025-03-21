from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Question(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')


class Answer(models.Model):
    name = models.CharField(max_length=300)  # User Answer
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")

    # In case user demands to generate quiz by possible answers this field is filled otherwise it's null.
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)


class QuizTopic(models.Model):
    """
    This is used to count Which Quiz Topic is most generated and provide leaderboard of popular quiz topics.
    """

    name = models.CharField(max_length=150)
    asked = models.PositiveIntegerField(default=1)
