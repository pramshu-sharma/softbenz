Steps to run the app:

1. Clone the repository.
2. Create a virtual environment in the cloned directory using virtualenv.
3. Add environment variables to the .env file for Django and the email backend.
  EMAIL_HOST_USER = <sender's email>
  EMAIL_HOST_PASSWORD = <sender's app password>
  App password may be required to send emails through Google.
  Check: https://support.google.com/accounts/answer/185833?hl=en
4. Install requirements. (pip install -r requirements.txt)
5. Migrate the database. (python manage.py makemigrations / migrate)
6. Create a superuser. (python manage.py createsuperuser)
7. Run the development server. (python manage.py runserver)
8. Login through the root URL: http://127.0.0.1:8000/

Features that were mentioned in the email can be found on the navbar of the application.
Screenshot:
![image](https://github.com/user-attachments/assets/3c967597-b393-49b4-a762-919b7aa2cc92)

URLs:
- / -  Login Form
- /admin/dashboard/ - Admin Dashboard
- /course/create/ - Course Creation
- /category/create/ - Category Creation
- /student/create/ - Student Registration
- /enrollment/create/ - Student Enrollment
- /student/dashboard/ - Non Super User Login Re-Direct i.e. Student.



 
  
