
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class AcademicSession(models.Model):
    name = models.CharField(max_length=20, unique=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Semester(models.Model):
    name = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name='semesters'
    )

    class Meta:
        unique_together = ('name', 'session')
        ordering = ['number']

    def __str__(self):
        return f"{self.name} - {self.session.name}"


class Course(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=150)
    credit = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.code} - {self.title}"
class CourseOffering(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='offerings'
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='course_offerings'
    )
    teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.PROTECT,
        related_name='course_offerings'
    )
    section = models.CharField(max_length=10, default='A')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'semester', 'section'],
                name='unique_course_semester_section'
            )
        ]

    def __str__(self):
        return f"{self.course.code} - {self.semester} - Section {self.section}"