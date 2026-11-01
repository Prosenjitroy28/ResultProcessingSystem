
from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        'teacher_id',
        'user',
        'department',
        'designation',
        'phone',
        'joining_date'
    )

    search_fields = (
        'teacher_id',
        'user__username',
        'designation'
    )

    list_filter = (
        'department',
        'designation'
    )
