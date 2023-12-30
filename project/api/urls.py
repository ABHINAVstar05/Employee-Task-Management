from django.urls import path

from taskapp.api_views import *

urlpatterns = [
    path('employee_management/', employee_management),
    path('task_management/', task_management),
    path('task_assignment/', task_assignment),
]