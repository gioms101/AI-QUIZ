from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Question, PossibleAnswer, QuizTopic
from .serializers import GenerateQuizSerializer, RetrieveQuestionSerializer, SaveAnswerSerializer, \
    PopularQuizTopicSerializer
from .utils import QuizGenerator
from .tasks import count_topics, delete_generated_quiz
from .permissions import ValidToGenerateQuiz
import ast


class GenerateQuizAPIView(GenericAPIView):
    """
    API endpoint to generate a quiz based on user prompt and return the first question ID.

    Accepts a prompt string and generates quiz questions with optional answers.
    Requires authentication and valid quiz generation permissions.
    """
    serializer_class = GenerateQuizSerializer
    permission_classes = [IsAuthenticated, ValidToGenerateQuiz]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_prompt = serializer.data.get('prompt')
        generated_quiz = QuizGenerator.generate_quiz(user_prompt)
        try:
            generated_quiz = ast.literal_eval(generated_quiz)
            if generated_quiz.get('message'):
                return Response(generated_quiz, status=status.HTTP_200_OK)
            has_possible_answers, topic_name = generated_quiz.pop("has_possible_answers", False), generated_quiz.pop(
                "topic_name", False)
            if has_possible_answers:
                for question in generated_quiz:
                    quest = Question.objects.create(name=question, user_id=request.user.id)
                    PossibleAnswer.objects.bulk_create([
                        PossibleAnswer(name=pos_answer, question_id=quest.id) for pos_answer in generated_quiz[question]
                    ])
            else:
                Question.objects.bulk_create([
                    Question(name=quest, user_id=request.user.id) for quest in generated_quiz
                ])
            if topic_name:
                count_topics.delay(topic_name)
            return Response({
                "status": "Created successfully",
                "question_id": Question.objects.filter(user_id=request.user.id).first().id
            }, status=status.HTTP_201_CREATED)

        except Exception:
            return Response("Something went Wrong.Please re-generate quiz!", status=status.HTTP_400_BAD_REQUEST)


class RetrieveQuestionAPIView(GenericAPIView):
    """
    API endpoint to retrieve a specific question and its possible answers for an authenticated user.

    This endpoint accepts a question ID as a URL parameter and returns the corresponding question
    along with its associated possible answers, if they exist. The question must belong to the
    authenticated user. If no matching question is found, it indicates the quiz has ended.

    URL Pattern:
        GET /questions/<pk>/

    Path Parameters:
        pk (int): The ID of the question to retrieve

    Returns:
        200 OK: Question data with possible answers if found
        204 No Content: When no question is found (quiz ended)
    """

    permission_classes = [IsAuthenticated]
    serializer_class = RetrieveQuestionSerializer

    def get(self, request, *args, **kwargs):
        quest_obj = Question.objects.prefetch_related('possible_answers').filter(id=self.kwargs.get('pk'),
                                                                                 user_id=
                                                                                 request.user.id)
        if quest_obj.exists():
            quest_obj = quest_obj.first()
            serializer = self.get_serializer(quest_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Message": "End of Quiz"}, status=status.HTTP_204_NO_CONTENT)


class SaveUserAnswerAPIView(CreateAPIView):
    """
    API Endpoint which saves user answer to the database.
    """
    serializer_class = SaveAnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ComputeQuizResult(GenericAPIView):
    """
    API endpoint to compute and return quiz results for an authenticated user.

    This endpoint processes a user's quiz questions and answers, computes the result
    using QuizGenerator, and returns the generated result. After successful computation,
    it triggers an asynchronous task to delete the user's generated quiz data.


    URL Pattern:
    POST /compute_quiz/

    Request Body:
        None required - uses authenticated user's existing questions and answers

    Returns:
        200 OK: Computed quiz results
        400 Bad Request: When result computation fails

    Raises:
        ValueError: If generated result cannot be parsed
        Exception: For other processing errors
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = User.objects.prefetch_related("questions", "answers").get(id=request.user.id)
        user_questions, user_answers = ([
                                        quest.name for quest in user.questions.all()
                                        ],
                                        [
                                        answer.name for answer in user.answers.all()
                                        ])
        generated_result = QuizGenerator.compute_quiz_result(user_questions, user_answers)
        try:
            generated_result = ast.literal_eval(generated_result)
            if generated_result:
                delete_generated_quiz.delay(user.id)
                return Response(generated_result, status=status.HTTP_200_OK)
        except Exception as e:
            Response(f"Something went wrong! {e}", status=status.HTTP_400_BAD_REQUEST)


class PopularQuizTopics(ListAPIView):
    """
    API endpoint to retrieve the top 5 most popular quiz topics.

    This endpoint returns a list of quiz topics ordered by popularity (number of times asked),
    limited to the top 5. It uses ListAPIView to provide standard list retrieval functionality.
    """
    queryset = QuizTopic.objects.all().order_by("-asked")[:5]
    serializer_class = PopularQuizTopicSerializer
