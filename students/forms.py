from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    """
    Form for student course enrollment.
    """
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),  # Initialize with empty queryset
        widget=forms.HiddenInput  # Hide this field in the form rendering
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set the course queryset to include all available courses.
        """
        super(CourseEnrollForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()