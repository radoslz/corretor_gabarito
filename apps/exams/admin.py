from django.contrib import admin

from .models import Exam, ExamApplication, StudentExamResult, StudentAnswer


class ExamApplicationInline(admin.TabularInline):
    model = ExamApplication
    extra = 0


class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "application_date",
        "question_count",
        "max_score",
        "is_active",
    )
    search_fields = ("title",)
    list_filter = ("subject", "application_date", "is_active")
    inlines = [ExamApplicationInline]


@admin.register(ExamApplication)
class ExamApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "exam",
        "class_group",
        "is_active",
        "created_at",
    )
    search_fields = (
        "exam__title",
        "class_group__name",
        "class_group__school__name",
    )
    list_filter = (
        "is_active",
        "class_group__school_year",
        "class_group__grade_level",
        "exam__subject",
    )


@admin.register(StudentExamResult)
class StudentExamResultAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "exam_application",
        "total_correct",
        "score",
        "percentage",
        "corrected_by",
        "corrected_at",
    )
    search_fields = (
        "student__name",
        "exam_application__exam__title",
        "exam_application__class_group__name",
    )
    list_filter = (
        "exam_application__exam__subject",
        "exam_application__exam__application_date",
        "exam_application__class_group__school_year",
        "exam_application__class_group__grade_level",
    )
    inlines = [StudentAnswerInline]


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ("result", "question_number", "is_correct")
    search_fields = (
        "result__student__name",
        "result__exam_application__exam__title",
    )
    list_filter = ("is_correct",)