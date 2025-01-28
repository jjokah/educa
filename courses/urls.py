from django.urls import path
from . import views


# URL patterns for the courses application
urlpatterns = [
    # Course List & Detail Views (Public)
    path(
        'list/',
        views.CourseListView.as_view(),
        name='course_list'
    ),

    # Instructor Course Management
    path(
        'mine/',
        views.ManageCourseListView.as_view(),
        name='manage_course_list'
    ),
    path(
        'create/',
        views.CourseCreateView.as_view(),
        name='course_create'
    ),

    # Module Management - Static paths first
    path(
        'module/order/',
        views.ModuleOrderView.as_view(),
        name='module_order'
    ),

    # Content Management - Static paths first
    path(
        'content/order',
        views.ContentOrderView.as_view(),
        name='content_order'
    ),

    # Module Content Management - More specific patterns
    path(
        'module/<int:module_id>/content/<model_name>/create/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_create'
    ),
    path(
        'module/<int:module_id>/content/<model_name>/<id>/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_update'
    ),
    path(
        'content/<int:id>/delete/',
        views.ContentDeleteView.as_view(),
        name='module_content_delete'
    ),
    path('module/<int:module_id>/',
        views.ModuleContentListView.as_view(),
        name='module_content_list'),

    # Course Management with dynamic parameters
    path(
        '<pk>/module/',
        views.CourseModuleUdpateView.as_view(),
        name='course_module_update'
    ),
    path(
        '<pk>/edit/',
        views.CourseUpdateView.as_view(),
        name='course_edit'
    ),
    path(
        '<pk>/delete',
        views.CourseDeleteView.as_view(),
        name='course_delete'
    ),

    # Subject and Course Detail - Most generic patterns last
    path(
        'subject/<slug:subject>/',
        views.CourseListView.as_view(),
        name='course_list_subject'
    ),
    path(
        '<slug:slug>/',
        views.CourseDetailView.as_view(),
        name='course_detail'
    ),   
]