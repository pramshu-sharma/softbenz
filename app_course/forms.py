from django.forms import (
    ModelForm,
    CharField,
    DateField,
    Textarea
)
from django.forms.widgets import DateInput

from .models import (
    Course,
    Category,
    Student,
    Enrollment
)
from .utils import MCQ_PLACEHOLDER


class CourseForm(ModelForm):
    quiz_mcq = CharField(
        widget=Textarea(attrs={'placeholder': MCQ_PLACEHOLDER}),
        required=False
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'category', 'video', 'document', 'quiz_mcq']


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        return self.cleaned_data.get('email')


class EnrollmentForm(ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'

    enrolled_date = DateField(widget=DateInput(attrs={'type': 'date'}))
