from django.db.models import Count
from rest_framework import serializers
from courses.models import Content, Course, Module, Subject


class ItemRelatedField(serializers.RelatedField):
    """
    Custom RelatedField that renders the related item using its render() method.
    Used for polymorphic content items like text, video, image etc.
    """
    def to_representation(self, value):
        return value.render()
    

class ContentSerializer(serializers.ModelSerializer):
    """
    Serializer for Course Content that includes the order and polymorphic item field.
    """
    item = ItemRelatedField(read_only=True)
    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Course Modules showing order, title and description.
    """
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """
    Extended Module serializer that includes all related content items.
    Used when full module details with contents are needed.
    """
    contents = ContentSerializer(many=True)
    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseSerializer(serializers.ModelSerializer):
    """
    Basic Course serializer including core fields and related modules.
    Modules are read-only to prevent nested writes.
    """
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'subject',
            'title',
            'slug',
            'overview',
            'created',
            'owner',
            'modules'
        ]


class CourseWithContentSerializer(serializers.ModelSerializer):
    """
    Detailed Course serializer that includes full module contents.
    Used when complete course data including all modules and their contents is needed.
    """
    modules = ModuleWithContentsSerializer(many=True)
    class Meta:
        model = Course
        fields = [
            'id',
            'subject',
            'title',
            'slug',
            'overview',
            'created',
            'owner',
            'modules'
        ]


class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subject model that converts Subject instances to JSON.
    """
    total_courses = serializers.IntegerField()
    popular_courses = serializers.SerializerMethodField()

    def get_popular_courses(self, obj):
        """
        Returns the top 3 courses with the most students,
        formatted as 'course_title (number_of_students)'
        """
        courses = obj.courses.annotate(
            total_students=Count('students')
        ).order_by('total_students')[:3]
        return [
            f'{c.title} ({c.total_students} {"student" if c.total_students == 1 else "students"})'
            for c in courses
        ]

    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug', 'total_courses', 'popular_courses']
