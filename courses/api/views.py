from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.api.pagination import StandardPagination
from courses.api.permissions import IsEnrolled
from courses.api.serializers import CourseSerializer, SubjectSerializer, CourseWithContentSerializer
from courses.models import Course, Subject


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for handling course-related operations.
    Provides read-only access to course data with pagination.
    """
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

    @action(
        detail=True,
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated]
    )
    def enroll(self, request, *args, **kwargs):
        """
        Endpoint to enroll authenticated users in a specific course.
        Returns confirmation of enrollment status.
        """
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})
    
    @action(
        detail=True,
        methods=['get'],
        serializer_class=CourseWithContentSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled]
    )
    def contents(self, request, *args, **kwargs):
        """
        Endpoint to retrieve course contents.
        Only accessible to authenticated users who are enrolled in the course.
        """
        return self.retrieve(request, *args, **kwargs)


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for handling subject-related operations.
    Provides read-only access to subject data with course count annotation and pagination.
    """
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination
