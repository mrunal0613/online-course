from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Course, Question, Choice, Submission, SubmissionAnswer


def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {"courses": courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "courses/course_details_bootstrap.html", {"course": course})


@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = Question.objects.filter(lesson__course=course).distinct()
    total = questions.count()

    if total == 0:
        messages.error(request, "This course does not have any exam questions yet.")
        return redirect("course_details", course_id=course.id)

    attempt = Submission.objects.create(
        user=request.user if request.user.is_authenticated else None,
        course=course,
        total_questions=total,
    )

    score = 0
    for question in questions:
        selected_id = request.POST.get(f"question_{question.id}")
        selected = Choice.objects.filter(pk=selected_id, question=question).first()
        correct = bool(selected and selected.is_correct)
        if correct:
            score += 1
        SubmissionAnswer.objects.create(
            submission=attempt,
            question=question,
            selected_choice=selected,
            is_correct=correct,
        )

    attempt.score = score
    attempt.save(update_fields=["score"])
    return redirect("show_exam_result", submission_id=attempt.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.prefetch_related("answers__question", "answers__selected_choice"),
        pk=submission_id,
    )
    return render(request, "courses/exam_result.html", {"submission": submission})
