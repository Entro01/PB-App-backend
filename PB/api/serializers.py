import re
from rest_framework import serializers
from .models import Employee, Enquiry

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def validate_employee_id(self, value):
        pattern = r'^PB-(AM|PC|FR)-[A-Z0-9]{4}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("invalid employee_id")
        return value


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'
