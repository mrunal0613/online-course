# Online Course Application with Exam Assessment

A Django starter project containing courses, lessons, multiple-choice questions,
exam submission, automatic evaluation, and an exam-result page.

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and the admin panel at
http://127.0.0.1:8000/admin/.

## Add sample content

After creating a superuser, use the Django admin to create a Course, add Lessons,
then add Questions and Choices linked to a lesson. Mark the correct Choice for
each question. Visit the course page and take the mock exam.

## GitHub submission

Create a **public** repository, upload the project files, and use the GitHub
file pages for the requested URLs. Do not submit the ZIP download URL as a
replacement for the individual file URLs.
