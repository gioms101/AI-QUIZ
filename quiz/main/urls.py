from django.urls import path

from .views import GenerateQuizAPIView, RetrieveQuestionAPIView

urlpatterns = [
    path("generate_quiz/", GenerateQuizAPIView.as_view(), name='generate-quiz'),
    path("questions/<int:pk>/", RetrieveQuestionAPIView.as_view(), name='get-question'),
]
