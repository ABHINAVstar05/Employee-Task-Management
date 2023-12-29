from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Employee)
admin.site.register(Subordinate)
admin.site.register(Lead)
admin.site.register(Task)