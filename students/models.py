
from django.db import models
from django.conf import settings
from academics.models import Department, AcademicSession, CourseOffering

class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT
    )

    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT
    )

    enrollment_date = models.DateField()

    def __str__(self):
        return f"{self.student_id} - {self.user.username}"
class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    course_offering = models.ForeignKey(
        CourseOffering,
        on_delete=models.PROTECT,
        related_name='enrollments'
    )

    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course_offering'],
                name='unique_student_course_enrollment'
            )
        ]

    def __str__(self):
        return (
            f"{self.student.student_id} - "
            f"{self.course_offering.course.code}"
        )