from django.urls import path
from . import views

app_name = "schools"

urlpatterns = [
    path("", views.school_list_view, name="school_list"),
    path("new/", views.school_create_view, name="school_create"),

    path("class-groups/", views.class_group_list_view, name="classgroup_list"),
    path("class-groups/new/", views.class_group_create_view, name="classgroup_create"),
    path("class-groups/<int:pk>/", views.class_group_detail_view, name="classgroup_detail"),
    path("class-groups/<int:pk>/edit/", views.class_group_update_view, name="classgroup_update"),

    path("students/", views.student_list_view, name="student_list"),
    path("students/new/", views.student_create_view, name="student_create"),
    path("students/<int:pk>/edit/", views.student_update_view, name="student_update"),
    path("students/import/", views.student_import_view, name="student_import"),
]