from rest_framework import serializers
from .models import Employee, EmployeeStatus

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_id', 'role', 'email', 'contact_number', 'address', 'pincode']

class EmployeeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeStatus
        fields = ['employee', 'is_online']