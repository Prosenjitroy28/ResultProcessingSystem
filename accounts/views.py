from academics.models import Department, Course, AcademicSession
from students.models import Student
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
                messages.error(request, 'Your account has no assigned role.')
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def teacher_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'TEACHER':
        messages.error(request, 'Access denied.')
        return redirect('login')

    return render(request, 'accounts/teacher_dashboard.html')


@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'STUDENT':
        messages.error(request, 'Access denied.')
        return redirect('login')

    return render(request, 'accounts/student_dashboard.html')

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
