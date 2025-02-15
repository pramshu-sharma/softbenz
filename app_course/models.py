from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.utils import timezone

from .utils import (
    CategoryPriority,
    validate_video_file_size,
    validate_document_file_size,
    validate_mcq,
)


class Category(models.Model):
    title = models.CharField(max_length=20, unique=True)
    priority = models.CharField(max_length=25, choices=[
        (priority.name, priority.value) for priority in CategoryPriority
    ])
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='subcategories')

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00')),
        MaxValueValidator(Decimal('9999.99'))
    ])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='course_category')
    document = models.FileField(upload_to='course_document/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)
    video = models.FileField(upload_to='course_video/',
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])], null=True, blank=True)
    quiz_mcq = models.JSONField(null=True, blank=True)
    create_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.video:
            validate_video_file_size(self.video)
        if self.document:
            validate_document_file_size(self.document)
        if self.quiz_mcq:
            validate_mcq(self.quiz_mcq)


class Student(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollment_student', default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment_course', default=1)
    enrolled_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'course')
