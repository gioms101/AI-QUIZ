from celery import shared_task
from .models import QuizTopic


@shared_task
def count_topics(topic_name):
    obj = QuizTopic.objects.filter(name=topic_name)
    if obj.exists():
        obj = obj.first()
        obj.asked += 1
        obj.save(update_fields=["asked"])
    else:
        QuizTopic.objects.create(name=topic_name)
