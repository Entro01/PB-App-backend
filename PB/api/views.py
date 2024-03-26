# employees/views.pys import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import Employee, EmployeeStatus
from .serializers import EmployeeSerializer, EmployeeStatusSerializer

class LoginView(APIView):
    def post(self, request):
        employee_id = request.data.get('employee_id')
        password = request.data.get('password')
        try:
            # Attempt to authenticate the user
            employee = Employee.objects.get(employee_id=employee_id) 
            if employee.contact_number == password:
                serializer = EmployeeSerializer(employee)
                return Response({'status': 'success', 'role': employee.role}, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'status': 'error', 'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({'status': 'error', 'message': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

class EmployeeStatusView(APIView):
    def get(self, request):
        employee_id = request.data.get('employee_id')
        try:
            status_value = EmployeeStatus.objects.get(employee_id=employee_id).is_online
            return Response({'status': status_value}, status=status.HTTP_200_OK)
        except EmployeeStatus.DoesNotExist:
            return Response({'status': 'error', 'message': 'Employee status not found'}, status=status.HTTP_404_NOT_FOUND)
        
class EmployeeStatusUpdateView(APIView):
    def post(self, request):
        employee_id = request.data.get('employee_id')
        is_online = request.data.get('is_online') == '1'
        try:
            status_obj = EmployeeStatus.objects.get(employee_id=employee_id)
            status_obj.is_online = is_online
            status_obj.save()
            serializer = EmployeeStatusSerializer(status)
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except EmployeeStatus.DoesNotExist:
            return Response({'status': 'error', 'message': 'Employee status not found'}, status=status.HTTP_404_NOT_FOUND)

class EmployeeCreateView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            # Create a corresponding EmployeeStatus instance
            EmployeeStatus.objects.create(employee_id=employee.employee_id, is_online=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PrintEmployeeStatusesView(APIView):
    def get(self, request):
        employee_statuses = EmployeeStatus.objects.all()
        employee = Employee.objects.all()
        response_data = []
        for status in employee:
            response_data.append({
                "id": status.id,
                "employee_id": status.employee_id,
                "role": status.role,
                "password": status.contact_number
            })
        for status in employee_statuses:
            response_data.append({
                "id": status.id,
                "employee_id": status.employee_id,
                "is_online": status.is_online
            })
        return Response(response_data)