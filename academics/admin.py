from .models import Department, AcademicSession, Semester, Course, CourseOffering
from django.contrib import admin
from .models import Department, AcademicSession, Semester, Course


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_year', 'end_year', 'is_active')
    list_filter = ('is_active',)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'session')
    list_filter = ('session',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'credit')
    list_filter = ('department',)
    search_fields = ('code', 'title')
@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester', 'teacher', 'section')
    list_filter = ('semester', 'teacher')
    search_fields = ('course__code', 'course__title', 'teacher__teacher_id')