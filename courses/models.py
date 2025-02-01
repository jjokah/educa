"""
Models for the courses application.
This module defines the database models for managing an online education platform,
including subjects, courses, modules and different types of content.
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

from .fields import OrderField


class Subject(models.Model):
    """
    Model representing a Subject/Category for courses.
    
    Attributes:
        title (str): The name of the subject
        slug (str): URL-friendly version of the title, unique across subjects
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Course(models.Model):
    """
    Model representing a Course within the platform.
    
    Attributes:
        owner (User): The instructor who created the course
        subject (Subject): The subject category this course belongs to
        students (User): The students enrolled in the course
        title (str): The name of the course
        slug (str): URL-friendly version of the title, unique across courses
        overview (str): Detailed description of the course
        created (datetime): Timestamp when the course was created
    """
    owner = models.ForeignKey(
        User,
        related_name="courses_created",
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, 
        related_name="courses", 
        on_delete=models.CASCADE
    )
    students = models.ManyToManyField(
        User,
        related_name='courses_joined',
        blank=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Module(models.Model):
    """
    Model representing a Module within a Course.
    
    Attributes:
        course (Course): The course this module belongs to
        title (str): The name of the module
        description (str): Detailed description of the module
        order (int): Custom ordering field for arranging modules within a course
    """
    course = models.ForeignKey(
        Course, related_name="modules", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"


class Content(models.Model):
    """
    Generic content model that can be associated with different types of content (text, video, etc.).
    Uses Django's ContentTypes framework for polymorphic relationships.
    
    Attributes:
        module (Module): The module this content belongs to
        content_type (ContentType): Type of content (text, video, image, or file)
        object_id (int): ID of the related content object
        item (GenericForeignKey): Generic foreign key to the actual content item
        order (int): Custom ordering field for arranging content within a module
    """
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text", "video", "image", "file")},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["module"])

    class Meta:
        ordering = ["order"]


class ItemBase(models.Model):
    """
    Abstract base class for all types of content items.
    
    Attributes:
        owner (User): The user who created this content
        title (str): Title of the content item
        created (datetime): When the item was created
        updated (datetime): When the item was last updated
    """
    owner = models.ForeignKey(
        User, related_name="%(class)s_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    
    def render(self):
        """
        Renders the content item using a template specific to its type.
        """
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self}
        )


class Text(ItemBase):
    """Content type for text-based content."""
    content = models.TextField()


class File(ItemBase):
    """Content type for file attachments."""
    file = models.FileField(upload_to="files")


class Image(ItemBase):
    """Content type for image content."""
    file = models.FileField(upload_to="images")


class Video(ItemBase):
    """Content type for video content, stored as URLs."""
    url = models.URLField()
