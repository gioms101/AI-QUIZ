from django.urls import path

from .views import GenerateQuizAPIView, RetrieveQuestionAPIView, SaveUserAnswerAPIView, ComputeQuizResult, \
    PopularQuizTopics

urlpatterns = [
    path("generate_quiz/", GenerateQuizAPIView.as_view(), name='generate-quiz'),
    path("questions/<int:pk>/", RetrieveQuestionAPIView.as_view(), name='get-question'),
    path("save_answer/", SaveUserAnswerAPIView.as_view(), name='save-answer'),
    path("compute_quiz/", ComputeQuizResult.as_view(), name='compute-quiz'),
    path("popular_topics/", PopularQuizTopics.as_view(), name='popular-topic'),
]
