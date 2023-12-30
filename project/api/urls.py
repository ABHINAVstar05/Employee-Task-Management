from django.urls import path

from taskapp.views import *

urlpatterns = [
    path('employee_management/', employee_management),
    path('task_management/', task_management),
]