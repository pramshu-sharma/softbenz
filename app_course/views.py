from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView

from .forms import CategoryForm, CourseForm, EnrollmentForm, StudentForm
from .models import Category, Course, Enrollment, Student
from .utils import generate_password, send_password_email


class SuperUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('student_dashboard')
        return redirect('login')


class CourseCreateView(SuperUserMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'admin_courses.html'
    success_url = reverse_lazy('create_course')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Course created successfully!')
        return response


class CategoryCreateView(SuperUserMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin_category.html'
    success_url = reverse_lazy('create_category')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Category created successfully!')
        return response


class StudentCreateView(SuperUserMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'admin_create_student.html'
    success_url = reverse_lazy('create_student')

    def form_valid(self, form):
        try:
            password = generate_password()
            student = form.save(commit=False)
            student.set_password(password)
            student.save()
            send_password_email(student, password)
            response = super().form_valid(form)
            messages.success(self.request, 'Student created successfully!')
            return response
        except IntegrityError:
            form.add_error(None, 'A student with this email already exists.')
            return self.form_invalid(form)


class EnrollmentCreateView(SuperUserMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'admin_enroll_student.html'
    success_url = reverse_lazy('create_enrollment')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Student Enrolled successfully!')
        return response


class AdminDashboardView(SuperUserMixin, ListView):
    model = Enrollment
    template_name = 'admin_dashboard.html'
    context_object_name = 'enrollments'


class AppLoginView(LoginView):
    template_name = 'login.html'

    def get_redirect_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('admin_dashboard')
        else:
            return reverse_lazy('student_dashboard')


class AppLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class StudentDashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'student_dashboard.html')
