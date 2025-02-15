from django.urls import path

from .views import (
    CategoryCreateView,
    CourseCreateView,
    StudentCreateView,
    EnrollmentCreateView,
    AdminDashboardView,
    AppLoginView,
    AppLogoutView,
    StudentDashboardView
)


urlpatterns = [
    path('', AppLoginView.as_view(), name='login'),
    path('logout/', AppLogoutView.as_view(), name='logout'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('course/create/', CourseCreateView.as_view(), name='create_course'),
    path('category/create/', CategoryCreateView.as_view(), name='create_category'),
    path('student/create/', StudentCreateView.as_view(), name='create_student'),
    path('enrollment/create', EnrollmentCreateView.as_view(), name='create_enrollment'),
]

