from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """
    Custom permission class to check if a user is enrolled in a course.
    """
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()
