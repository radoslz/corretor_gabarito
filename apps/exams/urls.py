from django.urls import path
from . import views

app_name = "exams"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("list/", views.exam_list_view, name="exam_list"),
    path("new/", views.exam_create_view, name="exam_create"),
    path("<int:pk>/edit/", views.exam_update_view, name="exam_update"),
    path("<int:pk>/applications/", views.exam_application_manage_view, name="exam_application_manage"),
    path("applications/<int:application_id>/correction/", views.correction_select_student_view, name="correction_select_student"),
    path("applications/<int:application_id>/correction/<int:student_id>/", views.correction_student_view, name="correction_student"),
    path("<int:pk>/report/", views.exam_report_view, name="exam_report"),
    path("<int:pk>/export/results/", views.export_exam_results_excel_view, name="export_exam_results_excel"),
    path("<int:pk>/export/summary/", views.export_exam_summary_excel_view, name="export_exam_summary_excel"),
]