from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from academics.models import Department, Course, AcademicSession, CourseOffering
from students.models import Student, Enrollment
from teachers.models import Teacher
from marks.models import Mark


# LOGIN
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.is_superuser and not hasattr(user, 'profile'):
                messages.error(
                    request,
                    'Your account has no assigned role.'
                )
                return redirect('login')

            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')

            if user.profile.role == 'ADMIN':
                return redirect('admin_dashboard')

            elif user.profile.role == 'TEACHER':
                return redirect('teacher_dashboard')

            elif user.profile.role == 'STUDENT':
                return redirect('student_dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


# LOGOUT
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# TEACHER DASHBOARD
@login_required
def teacher_dashboard(request):

    if (
        not hasattr(request.user, 'profile')
        or request.user.profile.role != 'TEACHER'
    ):
        messages.error(request, 'Access denied.')
        return redirect('login')

    teacher = Teacher.objects.filter(
        user=request.user
    ).first()

    if teacher is None:
        messages.error(
            request,
            'Teacher profile not found. Please contact the administrator.'
        )
        return redirect('login')

    courses = CourseOffering.objects.filter(
        teacher=teacher
    ).select_related(
        'course',
        'semester'
    ).annotate(
        total_students=Count(
            'enrollments__student',
            distinct=True
        )
    )

    enrollments = Enrollment.objects.filter(
        course_offering__teacher=teacher
    )

    context = {
        'teacher': teacher,

        'total_courses': courses.count(),

        'total_students': enrollments.values(
            'student'
        ).distinct().count(),

        'total_marks': Mark.objects.filter(
            enrollment__in=enrollments
        ).count(),

        'courses': courses,
    }

    return render(
        request,
        'accounts/teacher_dashboard.html',
        context
    )


# STUDENT DASHBOARD
@login_required
def student_dashboard(request):

    if (
        not hasattr(request.user, 'profile')
        or request.user.profile.role != 'STUDENT'
    ):
        messages.error(request, 'Access denied.')
        return redirect('login')

    return render(
        request,
        'accounts/student_dashboard.html'
    )


# ADMIN DASHBOARD
@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        if (
            not hasattr(request.user, 'profile')
            or request.user.profile.role != 'ADMIN'
        ):
            messages.error(request, 'Access denied.')
            return redirect('login')

    context = {
        'total_students': Student.objects.count(),
        'total_departments': Department.objects.count(),
        'total_courses': Course.objects.count(),
        'total_sessions': AcademicSession.objects.count(),
    }

    return render(
        request,
        'accounts/admin_dashboard.html',
        context
    )