from rest_framework.decorators import api_view
from rest_framework.response import Response

from taskapp.models import *
from taskapp.serializers import *

# Create your views here.


# Helper function to automatically populate the Lead and Subordinate tables
# when corresponding Employee is created.
def fill_role(obj, data) :
    if data['role'] == 'Lead' :
        Lead.objects.create(employee=obj)
    elif data['role'] == 'Subordinate' :
        Subordinate.objects.create(employee=obj)
    else :
        raise ValueError("Role must be 'Lead' or 'Subordinate'")
    

# API endpoint for Employee Management.
    
"""
1.) Used to fetch employee details like name, email and role.
2.) Used to create new employee and automatically populate the
    corresponding subordinate or lead table as per the employee role.
3.) Delete particular employee(s).
"""

@api_view(['GET', 'POST', 'DELETE'])
def employee_management(request) :
    
    if request.method == 'GET' :
        emp = Employee.objects.all()
        serialized = EmployeeSerializer(emp, many=True)
        return Response(serialized.data)

    elif request.method == 'POST' :
        data = request.data
        deserialized = EmployeeSerializer(data = data)
        if deserialized.is_valid() :
            deserialized.save()
            obj = Employee.objects.get(email = data['email'])
            fill_role(obj, data)
            return Response(deserialized.data)
        else :
            return Response(deserialized.errors)
        
    elif request.method == 'DELETE' :
        data = request.data
        try :
            obj = Employee.objects.get(email = data['email'])
            obj.delete()
            return Response({'Message: ': 'Employee deleted successfully.'})
        except Employee.DoesNotExist :
            errorMessage = 'Employee does not exist.'
            return Response(errorMessage)
        

# API endpoint for Task Management.
             
"""
1.) Used to fetch task information (title, deadline, associated subordinate and lead details).
2.) Used to add new task(s) with title, deadline and
    optional fields like the subordinate who is assigned this task and
    the lead who assigned that task to the subordinate.
3.) Delete particular task(s). 
"""

@api_view(['GET', 'POST', 'DELETE'])
def task_management(request) :
    if request.method == 'GET' :
        tasks = Task.objects.all()
        serialized = TaskSerializer(tasks, many = True)
        return Response(serialized.data)
    
    elif request.method == 'POST' :
        data = request.data
        deserialized = TaskSerializer(data = data)
        if deserialized.is_valid() :
            deserialized.save()
            return Response(deserialized.data)
        else :
            return Response(deserialized.errors)
        
    elif request.method == 'DELETE' :
        data = request.data
        try :
            obj = Task.objects.get(title = data['title'])
            obj.delete()
            return Response({'Message: ': 'Task deleted successfully.'})
        except Task.DoesNotExist :
            error_message = "Task does not exist."
            return Response(error_message)
        

# API endpoint for Task Assignment.

"""
1.) Used to see tasks which are not assigned to any subordinate.
2.) Used to assign the tasks to Subordinates by Leads.
"""

@api_view(['GET', 'POST'])
def task_assignment(request) :
    
    if request.method == 'GET' :
        tasks = Task.objects.filter(assigned_to__isnull=True)
        serialized = TaskSerializer(tasks, many=True)
        return Response(serialized.data)
    
    elif request.method == 'POST' :
        data = request.data
        print("**********", data['title'], data['assigned_to'], data['assigned_by'])

        task = Task.objects.filter(title = data['title'])

        subordinate = Employee.objects.get(email=data['assigned_to'])
        lead = Employee.objects.get(email=data['assigned_by'])
        subordinate_pk = subordinate.pk
        lead_pk = lead.pk

        try :
            subordinate = Subordinate.objects.get(pk=subordinate_pk)
        except Subordinate.DoesNotExist :
            error_message = "Enter correct subordinate email. Leads can assign task(s) to subordinates but not vice-versa."
            return Response(error_message)
        try :
            lead = Lead.objects.get(pk=lead_pk)
        except Lead.DoesNotExist :
            error_message = "Enter correct lead email. Leads can assign task(s) to subordinates but not vice-versa."
            return Response(error_message)

        task.update(assigned_to = subordinate, assigned_by = lead)


        return Response({'Status': f"Task: {data['title']} assigned to {data['assigned_to']} by {data['assigned_by']}"})

