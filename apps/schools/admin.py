from django.contrib import admin

from .models import School, ClassGroup, Student


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "is_active", "created_at")
    search_fields = ("name", "city")
    list_filter = ("is_active", "state")


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "grade_level",
        "shift",
        "school_year",
        "school",
        "responsible_teacher",
        "is_active",
    )
    search_fields = ("name", "school__name")
    list_filter = ("grade_level", "shift", "school_year", "is_active")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "class_group", "registration_number", "is_active", "created_at")
    search_fields = ("name", "registration_number", "class_group__name")
    list_filter = ("class_group__school_year", "class_group__grade_level", "is_active")