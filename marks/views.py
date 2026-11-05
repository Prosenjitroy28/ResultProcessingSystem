from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction

from teachers.models import Teacher
from academics.models import CourseOffering
from students.models import Enrollment
from .models import Mark


@login_required
def manage_marks(request, offering_id):

    # Check teacher permission
    if (
        not hasattr(request.user, 'profile')
        or request.user.profile.role != 'TEACHER'
    ):
        messages.error(request, 'Access denied.')
        return redirect('login')

    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    # Only allow the teacher's assigned course
    course = get_object_or_404(
        CourseOffering.objects.select_related(
            'course', 'semester'
        ),
        id=offering_id,
        teacher=teacher
    )

    enrollments = Enrollment.objects.filter(
        course_offering=course
    ).select_related(
        'student__user'
    ).order_by('student__student_id')

    if request.method == 'POST':

        pending_marks = []
        errors = []

        with transaction.atomic():

            for enrollment in enrollments:

                mark = Mark.objects.filter(
                    enrollment=enrollment
                ).first()

                if mark is None:
                    mark = Mark(enrollment=enrollment)

                try:
                    mark.attendance_marks = Decimal(
                        request.POST.get(
                            f'attendance_{enrollment.id}', '0'
                        )
                    )

                    mark.assignment_marks = Decimal(
                        request.POST.get(
                            f'assignment_{enrollment.id}', '0'
                        )
                    )

                    mark.class_test_marks = Decimal(
                        request.POST.get(
                            f'class_test_{enrollment.id}', '0'
                        )
                    )

                    mark.midterm_marks = Decimal(
                        request.POST.get(
                            f'midterm_{enrollment.id}', '0'
                        )
                    )

                    mark.final_marks = Decimal(
                        request.POST.get(
                            f'final_{enrollment.id}', '0'
                        )
                    )

                    mark.full_clean()
                    pending_marks.append(mark)

                except (InvalidOperation, ValueError, ValidationError) as error:
                    errors.append(
                        f"Invalid marks for student "
                        f"{enrollment.student.student_id}: {error}"
                    )

            if errors:
                for error in errors:
                    messages.error(request, error)

            else:
                for mark in pending_marks:
                    mark.save()

                messages.success(
                    request,
                    'Student marks saved successfully!'
                )

                return redirect(
                    'manage_marks',
                    offering_id=course.id
                )

    # Load existing marks
    for enrollment in enrollments:
        enrollment.existing_mark = Mark.objects.filter(
            enrollment=enrollment
        ).first()

    context = {
        'course': course,
        'enrollments': enrollments,
    }

    return render(
        request,
        'marks/manage_marks.html',
        context
    )