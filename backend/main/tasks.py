from celery import shared_task
from .models import QuizTopic, Question, Answer


@shared_task
def count_topics(topic_name):
    obj = QuizTopic.objects.filter(name=topic_name)
    if obj.exists():
        obj = obj.first()
        obj.asked += 1
        obj.save(update_fields=["asked"])
    else:
        QuizTopic.objects.create(name=topic_name)


@shared_task
def delete_generated_quiz(user_id):
    Question.objects.filter(user_id=user_id).delete()
