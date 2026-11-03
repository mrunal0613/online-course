from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import (
    Course,
    Lesson,
    Question,
    Choice,
    Enrollment,
    Submission,
)


def course_list(request):
    courses = Course.objects.all()

    return render(
        request,
        "course_list.html",
        {"course_list": courses, "courses": courses}
    )


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    return render(
        request,
        "course_details_bootstrap.html",
        {"course": course}
    )


@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Find the learner's enrollment.
    if not request.user.is_authenticated:
        messages.error(
            request,
            "Please log in before submitting the exam."
        )
        return redirect("course_details", course_id=course.id)

    enrollment = Enrollment.objects.filter(
        learner__user=request.user,
        course=course
    ).first()

    if enrollment is None:
        messages.error(
            request,
            "You must be enrolled in this course before taking the exam."
        )
        return redirect("course_details", course_id=course.id)

    questions = Question.objects.filter(course=course).order_by("order", "id")

    if not questions.exists():
        messages.error(request, "No exam questions are available.")
        return redirect("course_details", course_id=course.id)

    # Create the submission for this enrollment.
    submission = Submission.objects.create(
        enrollment=enrollment
    )

    total_score = 0

    for question in questions:
        selected_id = request.POST.get(
            f"question_{question.id}"
        )

        selected_choice = Choice.objects.filter(
            id=selected_id,
            question=question
        ).first()

        selected_ids = (
            [selected_choice.id]
            if selected_choice is not None
            else []
        )

        total_score += question.is_get_score(selected_ids)

        if selected_choice is not None:
            submission.choices.add(selected_choice)

    # Redirect with the required course and submission IDs.
    return redirect(
        "show_exam_result",
        course_id=course.id,
        submission_id=submission.id
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)

    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__course=course
    )

    questions = Question.objects.filter(course=course)

    score = 0
    max_score = 0
    exam_results = []

    for question in questions:
        max_score += question.grade

        selected_choices = submission.choices.filter(
            question=question
        )

        selected_ids = list(
            selected_choices.values_list("id", flat=True)
        )

        question_score = question.is_get_score(selected_ids)
        score += question_score

        exam_results.append({
            "question": question,
            "selected_choices": selected_choices,
            "score": question_score,
            "grade": question.grade,
            "is_correct": question_score == question.grade,
        })

    percentage = (
        round(score / max_score * 100)
        if max_score > 0
        else 0
    )

    context = {
        "course": course,
        "submission": submission,
        "score": score,
        "max_score": max_score,
        "percentage": percentage,
        "exam_results": exam_results,
        "passed": percentage >= 70,
    }

    return render(
        request,
        "exam_result_bootstrap.html",
        context
    )
