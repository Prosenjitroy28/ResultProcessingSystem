from django.db.models.signals import post_save
from django.dispatch import receiver

from marks.models import Mark
from .models import Result, SemesterGPA, OverallCGPA


@receiver(post_save, sender=Mark)
def update_student_results(sender, instance, **kwargs):

    enrollment = instance.enrollment
    student = enrollment.student
    semester = enrollment.course_offering.semester

    # Create or update Result
    result, created = Result.objects.get_or_create(
        mark=instance
    )

    if not created:
        result.save()

    # Create or update Semester GPA
    semester_gpa, created = SemesterGPA.objects.get_or_create(
        student=student,
        semester=semester
    )

    if not created:
        semester_gpa.save()

    # Create or update Overall CGPA
    overall_cgpa, created = OverallCGPA.objects.get_or_create(
        student=student
    )

    if not created:
        overall_cgpa.save()