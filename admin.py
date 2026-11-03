from django.contrib import admin
from django.contrib.auth.models import User
from .models import (
    Course,
    Lesson,
    Question,
    Choice,
    Submission,
    SubmissionAnswer,
    Enrollment,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "lesson", "order")
    list_filter = ("lesson__course",)
    search_fields = ("text",)
    inlines = [ChoiceInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title", "content")
    inlines = [QuestionInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    inlines = [LessonInline]


class SubmissionAnswerInline(admin.TabularInline):
    model = SubmissionAnswer
    extra = 0
    readonly_fields = ("question", "selected_choice", "is_correct")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "score", "total_questions", "submitted_at")
    readonly_fields = ("submitted_at",)
    inlines = [SubmissionAnswerInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at")
    list_filter = ("course",)


# User is already registered by Django's Authentication and Authorization app.
# The seven imported model classes above are Course, Lesson, Question, Choice,
# Submission, SubmissionAnswer, and Enrollment.
