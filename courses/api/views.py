from django.db.models import Count

from rest_framework import generics, viewsets

from courses.api.pagination import StandardPagination
from courses.api.serializers import CourseSerializer, SubjectSerializer
from courses.models import Course, Subject


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination


# class SubjectListView(generics.ListAPIView):
#     """
#     API view to retrieve a list of all subjects.
#     """
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))
#     serializer_class = SubjectSerializer
#     pagination_class = StandardPagination


# class SubjectDetailView(generics.RetrieveAPIView):
#     """
#     API view to retrieve details of a specific subject.
#     """
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))
#     serializer_class = SubjectSerializer
