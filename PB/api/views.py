from rest_framework import generics, permissions
from .models import Employee, EmployeeStatus
from .serializers import EmployeeSerializer, EmployeeStatusSerializer, LoginSerializer
from .authentication import EmployeeIDAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import serializers


class EmployeeLoginView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = LoginSerializer
    authentication_classes = [EmployeeIDAuthentication]
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        employee = serializer.save()
        print(f"Employee {employee.employee_id} logged in.")

class EmployeeStatusUpdateView(generics.UpdateAPIView):
    queryset = EmployeeStatus.objects.all()
    serializer_class = EmployeeStatusSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_object(self):
        # Extract employee_id from the request data
        employee_id = self.request.data.get('employee_id')
        if not employee_id:
            raise serializers.ValidationError("employee_id is required.")
    
        # Retrieve the EmployeeStatus object based on employee_id
        try:
            return EmployeeStatus.objects.get(employee_id=employee_id)
        except EmployeeStatus.DoesNotExist:
            raise serializers.ValidationError("Employee with the given employee_id does not exist.")

class EmployeeStatusListView(generics.ListAPIView):
    queryset = EmployeeStatus.objects.all()
    serializer_class = EmployeeStatusSerializer
    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]