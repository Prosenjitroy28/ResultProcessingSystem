from django.db import models
from decimal import Decimal
from students.models import Student
from academics.models import Semester
from marks.models import Mark


class Result(models.Model):

    mark = models.OneToOneField(
        Mark,
        on_delete=models.CASCADE,
        related_name='result'
    )

    letter_grade = models.CharField(
        max_length=2,
        blank=True
    )

    grade_point = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=10,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_grade(self):
        total = float(self.mark.total_marks)

        if total >= 80:
            return 'A+', 4.00
        elif total >= 75:
            return 'A', 3.75
        elif total >= 70:
            return 'A-', 3.50
        elif total >= 65:
            return 'B+', 3.25
        elif total >= 60:
            return 'B', 3.00
        elif total >= 55:
            return 'B-', 2.75
        elif total >= 50:
            return 'C+', 2.50
        elif total >= 45:
            return 'C', 2.25
        elif total >= 40:
            return 'D', 2.00
        else:
            return 'F', 0.00

    def save(self, *args, **kwargs):
        grade, point = self.calculate_grade()

        self.letter_grade = grade
        self.grade_point = point

        self.status = (
            'PASS' if grade != 'F' else 'FAIL'
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.mark.enrollment.student.student_id} - "
            f"{self.letter_grade}"
        )
class SemesterGPA(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='semester_gpas'
    )

    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='student_gpas'
    )

    gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    total_credits = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'semester'],
                name='unique_student_semester_gpa'
            )
        ]

    def calculate_gpa(self):

        results = Result.objects.filter(
            mark__enrollment__student=self.student,
            mark__enrollment__course_offering__semester=self.semester
        ).select_related(
            'mark__enrollment__course_offering__course'
        )

        total_points = Decimal('0')
        total_credits = Decimal('0')

        for result in results:

            credit = (
                result.mark.enrollment
                .course_offering.course.credit
            )

            total_points += result.grade_point * credit
            total_credits += credit

        if total_credits > 0:
            self.gpa = (
                total_points / total_credits
            ).quantize(Decimal('0.01'))
        else:
            self.gpa = Decimal('0.00')

        self.total_credits = total_credits

    def save(self, *args, **kwargs):
        self.calculate_gpa()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.student.student_id} - "
            f"{self.semester} - GPA: {self.gpa}"
        )
class OverallCGPA(models.Model):

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='overall_cgpa'
    )

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    total_credits = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0
    )

    calculated_at = models.DateTimeField(auto_now=True)

    def calculate_cgpa(self):
        semester_gpas = SemesterGPA.objects.filter(
            student=self.student
        )

        total_points = Decimal('0')
        total_credits = Decimal('0')

        for item in semester_gpas:
            total_points += item.gpa * item.total_credits
            total_credits += item.total_credits

        if total_credits > 0:
            self.cgpa = (
                total_points / total_credits
            ).quantize(Decimal('0.01'))
        else:
            self.cgpa = Decimal('0.00')

        self.total_credits = total_credits

    def save(self, *args, **kwargs):
        self.calculate_cgpa()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.student_id} - CGPA: {self.cgpa}"    