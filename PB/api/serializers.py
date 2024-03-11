from rest_framework import serializers
from .models import Employee, EmployeeStatus

class LoginSerializer(serializers.ModelSerializer):
    employee_id = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = Employee
        fields = ['employee_id', 'password']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'role', 'email', 'contact_number', 'address', 'pincode']

class EmployeeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeStatus
        fields = ['employee', 'is_online']