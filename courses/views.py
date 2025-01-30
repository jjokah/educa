from django.apps import apps
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms.models import modelform_factory
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

from students.forms import CourseEnrollForm

from .forms import ModuleFormSet
from .models import Course, Content, Module, Subject


class OwnerMixin:
    """
    Mixin to filter queryset to only show objects owned by the current user
    """
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    

class OwnerEditMixin:
    """
    Mixin to automatically set the owner of an object to the current user
    """
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Base mixin for Course views requiring ownership and authentication
    """
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    Mixin for editing Course objects with ownership validation
    """
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    """
    View to display list of courses owned by the current user
    """
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    View to create new course objects
    """
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    View to update existing course objects
    """
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """
    View to delete course objects
    """
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUdpateView(TemplateResponseMixin, View):
    """
    View to handle the update of course modules using a formset
    """
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        """
        Returns a ModuleFormSet instance for the current course
        """
        return ModuleFormSet(instance=self.course, 
                             data=data)
    
    def dispatch(self, request, pk):
        """
        Retrieves the course and validates ownership before processing the request
        """
        self.course = get_object_or_404(Course, id=pk, 
                                        owner=request.user)
        return super().dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests by displaying the formset
        """
        formset = self.get_formset()
        return self.render_to_response({
                                    'course': self.course,
                                    'formset': formset})
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests by processing the formset data
        """
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'formset': formset})
    

class CourseListView(TemplateResponseMixin, View):
    """
    View to display list of all courses with optional subject filtering
    """
    model = Course
    template_name = 'courses/course/list.html'
    def get(self, request, subject=None):
        """
        Retrieves courses and subjects with their counts
        """
        subjects = Subject.objects.annotate(
            total_courses=Count('courses')
        )
        courses = Course.objects.annotate(
            total_modules=Count('modules')
        )
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response(
            {
                'subjects': subjects,
                'subject': subject,
                'courses': courses
            }
        )
    

class CourseDetailView(DetailView):
    """
    View to display detailed information about a specific course
    """
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        """
        Extend context data to include course enrollment form
        """
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course':self.object}
        )
        return context
    

class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
    View to create and update course content items
    """
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        """
        Returns the appropriate content model based on model_name
        """
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None
    
    def get_form(self, model, *args, **kwargs):
        """
        Generates a model form excluding specific fields
        """
        Form = modelform_factory(model, exclude=['owner', 
                                                 'order', 
                                                 'created', 
                                                 'updated'])
        return Form(*args, **kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None):
        """
        Validates module ownership and retrieves content object if editing
        """
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)
    
    def get(self, request, module_id, model_name, id=None):
        """
        Handles GET requests by displaying the form for content creation/editing
        """
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})
    
    def post(self, request, module_id, model_name, id=None):
        """Handles POST requests by processing form data and saving content
        
        Creates new content if id is None, otherwise updates existing content.
        Sets the owner and associates content with the module.
        """
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View):
    """
    View to handle deletion of course content
    """
    def post(self, request, id):
        """
        Deletes content item after validating ownership
        """
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)
    

class ModuleContentListView(TemplateResponseMixin, View):
    """
    View to display list of contents for a specific module
    """
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        """
        Retrieves and displays module contents after ownership validation
        """
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response({'module': module})
    

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """
    View to handle AJAX requests for updating module order
    """
    def post(self, request):
        """
        Updates the order of modules based on received JSON data
        """
        for id, order in self.request_json.items():
            Module.objects.filter(
                id=id, course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})
        

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """
    View to handle AJAX requests for updating content order
    """
    def post(self, request):
        """
        Updates the order of content items based on received JSON data
        """
        for id, order in self.request_json.items():
            Content.objects.filter(
                id=id,module__course__owner=request.user
                ).update(order=order)
        return self.render_json_response({'saved': 'OK'})
    