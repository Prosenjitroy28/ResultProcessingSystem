from django.contrib import admin
from .models import Result, SemesterGPA, OverallCGPA

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = (
        'mark',
        'letter_grade',
        'grade_point',
        'status',
        'created_at'
    )

    search_fields = (
        'mark__enrollment__student__student_id',
        'mark__enrollment__student__user__username',
        'mark__enrollment__course_offering__course__code'
    )

    list_filter = (
        'letter_grade',
        'status',
        'mark__enrollment__course_offering__semester'
    )

    readonly_fields = (
        'letter_grade',
        'grade_point',
        'status',
        'created_at'
    )
@admin.register(SemesterGPA)
class SemesterGPAAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'semester',
        'gpa',
        'total_credits',
        'calculated_at',
    )

    search_fields = (
        'student__student_id',
        'student__user__username',
        'semester__name',
    )

    list_filter = ('semester',)

    readonly_fields = (
        'gpa',
        'total_credits',
        'calculated_at',
    )    
@admin.register(OverallCGPA)
class OverallCGPAAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'cgpa',
        'total_credits',
        'calculated_at',
    )

    search_fields = (
        'student__student_id',
        'student__user__username',
    )

    readonly_fields = (
        'cgpa',
        'total_credits',
        'calculated_at',
    )    