from django.db import models

# Create your models here.

class Employee(models.Model):
    
    ROLE_CHOICES = [
        ('Lead', 'Lead'),
        ('Subordinate', 'Subordinate'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Subordinate(models.Model):
    # Field to establish connection btween subordinate and employee models
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)

    # Other subordinate-specific fields
    assigned_tasks = models.ManyToManyField('Task', related_name='assigned_subordinates', blank=True)
    completed_tasks = models.ManyToManyField('Task', related_name='completed_subordinates', blank=True)
    unassigned_tasks = models.ManyToManyField('Task', related_name='unassigned_subordinates', blank=True)

    def __str__(self):
        return f"Subordinate: {self.employee}"
        

class Lead(models.Model):
    # Field to establish connection btween lead and employee models
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Lead: {self.employee}"
    

class Task(models.Model):
    title = models.CharField(max_length=255)
    deadline = models.DateField()
    assigned_to = models.ForeignKey(Subordinate, on_delete=models.SET_NULL, related_name='tasks_assigned', null=True, blank=True)
    assigned_by = models.ForeignKey(Lead, on_delete=models.SET_NULL, related_name='tasks_assigned', null=True, blank=True)

    def __str__(self):
        return self.title
    
