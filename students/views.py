from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from courses.models import Course
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


class StudentCourseListView(LoginRequiredMixin, ListView):
    """
    Display a list of courses that the current student is enrolled in.
    """
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    

class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    """
    Display detailed view of a specific course for enrolled students.
    """
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        """
        Ensure students can only view courses they are enrolled in.
        """
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    
    def get_context_data(self, **kwargs):
        """
        Add the current module to the template context.
        If no specific module is requested, defaults to the first module.
        """
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context
