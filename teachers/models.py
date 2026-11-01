
from django.db import models
from django.conf import settings
from academics.models import Department


class Teacher(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_record'
    )

    teacher_id = models.CharField(
        max_length=20,
        unique=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='teachers'
    )

    designation = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    joining_date = models.DateField()

    def __str__(self):
        return f"{self.teacher_id} - {self.user.username}"
