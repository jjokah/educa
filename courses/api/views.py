from rest_framework import generics
from courses.api.serializers import SubjectSerializer
from courses.models import Subject


class SubjectListView(generics.ListAPIView):
    """
    API view to retrieve a list of all subjects.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a specific subject.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

