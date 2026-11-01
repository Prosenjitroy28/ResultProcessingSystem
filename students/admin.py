
from django.contrib import admin
from .models import Student, Enrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'student_id',
        'user',
        'department',
        'session',
        'enrollment_date'
    )

    search_fields = (
        'student_id',
        'user__username'
    )

    list_filter = (
        'department',
        'session'
    )

    ordering = ('student_id',)
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course_offering',
        'enrollment_date'
    )

    search_fields = (
        'student__student_id',
        'student__user__username',
        'course_offering__course__code'
    )

    list_filter = (
        'course_offering__semester',
        'course_offering__teacher'
    )