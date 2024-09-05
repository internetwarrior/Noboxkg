from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, PostInteraction

@receiver(post_save, sender=Post)
def create_post_interaction(sender, instance, created, **kwargs):
    if created:
        PostInteraction.objects.create(post=instance)
