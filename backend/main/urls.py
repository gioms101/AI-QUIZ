from django.urls import path

from .views import GenerateQuizAPIView, RetrieveQuestionAPIView, SaveUserAnswerAPIView, ComputeQuizResult, \
    PopularQuizTopics, HaveAlreadyGeneratedQuiz, DeleteGeneratedQuiz, ReturnToUnfinishedQuiz

urlpatterns = [
    path("generate_quiz/", GenerateQuizAPIView.as_view(), name='generate-quiz'),
    path("questions/<int:pk>/", RetrieveQuestionAPIView.as_view(), name='get-question'),
    path("save_answer/", SaveUserAnswerAPIView.as_view(), name='save-answer'),
    path("compute_quiz/", ComputeQuizResult.as_view(), name='compute-quiz'),
    path("popular_topics/", PopularQuizTopics.as_view(), name='popular-topic'),
    path("have_already_generated_quiz/", HaveAlreadyGeneratedQuiz.as_view()),
    path("delete_user_quiz/", DeleteGeneratedQuiz.as_view()),
    path("get_question_id/", ReturnToUnfinishedQuiz.as_view()),
]
