from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "",
        views.course_list,
        name="course_list"
    ),

    path(
        "course/<int:course_id>/",
        views.course_details,
        name="course_details"
    ),

    path(
        "<int:course_id>/submit/",
        views.submit,
        name="submit"
    ),

    path(
        "<int:course_id>/exam/<int:submission_id>/",
        views.show_exam_result,
        name="show_exam_result"
    ),
]
