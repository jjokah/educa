from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    """
    Signal receiver function that updates the total likes count for an Image instance
    when the many-to-many relationship 'users_like' changes.
    """
    instance.total_likes = instance.users_like.count()
    instance.save()
