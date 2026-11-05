from django.urls import path
from . import views

urlpatterns = [
    path(
        'course/<int:offering_id>/',
        views.manage_marks,
        name='manage_marks'
    ),
]