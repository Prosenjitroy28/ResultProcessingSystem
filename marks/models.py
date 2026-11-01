from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from students.models import Enrollment


class Mark(models.Model):

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='mark'
    )

    attendance_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )

    assignment_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    class_test_marks = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default=0,
    validators=[MinValueValidator(0), MaxValueValidator(10)]
)
    midterm_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(30)
        ]
    )

    final_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(40)
        ]
    )

    total_marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_marks = (
            self.attendance_marks
            + self.assignment_marks
            + self.class_test_marks
            + self.midterm_marks
            + self.final_marks
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.enrollment.student.student_id} - "
            f"{self.enrollment.course_offering.course.code}"
        )