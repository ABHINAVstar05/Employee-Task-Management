from rest_framework.decorators import api_view
from rest_framework.response import Response

from taskapp.models import *
from taskapp.serializers import *

# Create your views here.


# Automatically populate the Lead and Subordinate tables when corresponding Employee is created.
def fill_role(obj, data) :
    if data['role'] == 'Lead' :
        Lead.objects.create(employee=obj)
    elif data['role'] == 'Subordinate' :
        Subordinate.objects.create(employee=obj)
    else :
        raise ValueError("Role must be 'Lead' or 'Subordinate'")
    


@api_view(['GET', 'POST', 'DELETE'])
def emp(request) :
    
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