from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView

from .forms import CourseEnrollForm


class StudentRegistrationView(CreateView):
    """
    View for handling new student registration
    """
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        """
        Handle valid form submission
        """
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'], password=cd['password1']
        )
        login(self.request, user)
        return result
    

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """
    View for handling course enrollment for authenticated students.
    """
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        """
        Handle valid form submission by adding the student to the course.
        """
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Determine URL to redirect to after successful enrollment.
        """
        return reverse_lazy(
            'student_course_detail', args=[self.course.id]
        )
    