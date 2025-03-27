from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission


class ValidToGenerateQuiz(BasePermission):
    message = "You already generated quiz"

    def has_permission(self, request, view):
        user = User.objects.prefetch_related('questions').get(id=request.user.id)
        return not user.questions.all()
