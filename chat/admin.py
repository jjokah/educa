from django.contrib import admin
from chat.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for Message model.
    """
    # Configure which fields to display in the list view
    list_display = ['sent_on', 'user', 'course', 'content']
    # Add filters in the right sidebar
    list_filter = ['sent_on', 'course']
    # Enable search functionality for message content
    search_fields = ['content']
    # Use raw_id widget for selecting related user and course
    # Helps with performance when there are many users/courses
    raw_id_fields = ['user', 'course']
