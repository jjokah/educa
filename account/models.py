"""Models for user accounts and relationships."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    """Extends the built-in User model"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True
    )

    def __str_(self):
        return f'Profile of {self.user.username}'


class Contact(models.Model):
    """Tracks user follow relationships (intermediate model)."""

    # User who initiates the follow
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_from_set',
        on_delete=models.CASCADE
    )
    # User being followed
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_to_set',
        on_delete=models.CASCADE
    )
    # Timestamp of when the follow relationship was created
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'
    

# Dynamically add field to User model (monkey patching, not recommended)
# - leverage built-in User model to avoid creating a custom one.
user_model = get_user_model()
user_model.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Contact,
        related_name='followers',
        symmetrical=False # following isn't automatically mutual
    )
)

