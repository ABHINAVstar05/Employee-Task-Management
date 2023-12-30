from rest_framework import serializers

from taskapp.models import *


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class SubordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subordinate
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    subordinate_info = SubordinateSerializer(source='subordinate', read_only=True)
    class Meta:
        model = Employee
        fields = ['name', 'email', 'role', 'subordinate_info']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        depth = 1