from django.contrib import admin
from .models import Mark


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):

    list_display = (
        'enrollment',
        'attendance_marks',
        'assignment_marks',
        'class_test_marks',
        'midterm_marks',
        'final_marks',
        'total_marks',
        'updated_at'
    )

    search_fields = (
        'enrollment__student__student_id',
        'enrollment__student__user__username',
        'enrollment__course_offering__course__code'
    )

    list_filter = (
        'enrollment__course_offering__semester',
        'enrollment__course_offering__teacher'
    )

    readonly_fields = (
        'total_marks',
        'created_at',
        'updated_at'
    )