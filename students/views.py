
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Student
from results.models import Result, SemesterGPA, OverallCGPA
from academics.models import Semester


@login_required
def student_dashboard(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    results = Result.objects.filter(
        mark__enrollment__student=student
    ).select_related(
        'mark__enrollment__course_offering__course',
        'mark__enrollment__course_offering__semester'
    )

    # Get semesters that have results for this student
    semester_ids = results.values_list(
        'mark__enrollment__course_offering__semester_id',
        flat=True
    ).distinct()

    semesters = Semester.objects.filter(
        id__in=semester_ids
    ).order_by('number')

    # Filter results by selected semester
    selected_semester_id = request.GET.get('semester')

    if selected_semester_id:
        results = results.filter(
            mark__enrollment__course_offering__semester_id=selected_semester_id
        )

    # Get semester GPA records
    semester_gpas = SemesterGPA.objects.filter(
        student=student
    ).select_related('semester')

    # Get overall CGPA
    overall_cgpa, created = OverallCGPA.objects.get_or_create(
        student=student
    )

    if not created:
        overall_cgpa.save()

    context = {
        'student': student,
        'results': results,
        'semesters': semesters,
        'selected_semester_id': selected_semester_id,
        'semester_gpas': semester_gpas,
        'overall_cgpa': overall_cgpa,
    }

    return render(
        request,
        'students/student_dashboard.html',
        context
    )
