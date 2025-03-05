from django.conf import settings
from django.db import models


class Message(models.Model):
    """
    Represents a chat message in the course discussion system.
    """
    # Link to the user who sent the message
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='chat_messages'
    )
    # Associate message with specific course
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.PROTECT,
        related_name='chat_messages'
    )
    # The actual message text
    content = models.TextField()
    # Automatically set timestamp when message is created
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} on {self.course} at {self.sent_on}'
