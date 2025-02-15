import random
import string
from enum import Enum

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail


class CategoryPriority(Enum):
    low = 'Low'
    medium = 'Medium'
    high = 'High'


def validate_video_file_size(file):
    max_file_size = 51200
    if file.size > max_file_size * 1024:
        raise ValidationError('File size for videos must not exceed 50 MB.')


def validate_document_file_size(file):
    max_file_size = 10240
    if file.size > max_file_size * 1024:
        raise ValidationError('File size for documents must not exceed 10 MB.')


def generate_password(length=8):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for i in range(length))


def send_password_email(student, password):
    subject = 'Your Student Password'
    message = f'''
    Hi {student.first_name} {student.last_name},
    Your account has been created successfully.

    Your password: {password}

    Please keep this information secure.
    '''
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student.email], fail_silently=False)


def validate_mcq(mcq):
    for key, value in mcq.items():
        if 'question' not in value or not isinstance(value['question'], str):
            raise ValidationError(f'Question: {key} must contain a "question" of type: String.')

        if 'options' not in value or not isinstance(value['options'], dict):
            raise ValidationError(f'Question: {key} must contain "options" of type: Dictionary / Object.')

        if 'solution' not in value or not isinstance(value['solution'], str):
            raise ValidationError(f'Question: {key} must contain a "solution" of type: String.')

        for option_key, option_value in value['options'].items():
            if not isinstance(option_key, str) or len(option_key) != 1 or option_key not in 'ABCD':
                raise ValidationError(
                    f'Invalid option key "{option_key}" in question {key}. Must be "A", "B", "C", or "D".')
            if not isinstance(option_value, str):
                raise ValidationError(f'Option value for "{option_key}" in question {key} must be a string.')

        valid_solutions = ['A', 'B', 'C', 'D']
        solutions = [solution.strip() for solution in value['solution'].split(',')]
        if any(solution not in valid_solutions for solution in solutions):
            raise ValidationError(
                f'Invalid solution format in question {key}. Must contain "A", "B", "C", or "D", separated by commas.')


MCQ_PLACEHOLDER = '''{
    1: {
        "question": "Question1?",
        "options": {
            "A": "a",
            "B": "b",
            "C": "c",
            "D": "d"
        },
        "solution": "A, B"
    },
    2: {
        "question": "Question2?",
        "options": {
            "A": "a",
            "B": "b",
            "C": "c",
            "D": "d"
        },
        "solution": "C, D"
    }
}'''
