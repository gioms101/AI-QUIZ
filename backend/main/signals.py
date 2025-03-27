from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Answer


@receiver(post_save, sender=Answer)
def save_question_detail(sender, instance, created, **kwargs):
    if created:
        question_obj = instance.question
        question_obj.is_answered = True
        question_obj.save(update_fields=['is_answered'])
