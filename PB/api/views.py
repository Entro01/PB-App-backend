# employees/views.pys import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer
from django.shortcuts import get_object_or_404

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
        employee_id = request.GET.get('employee_id', None)
        try:
            status_value = Employee.objects.get(employee_id=employee_id).is_online
            return Response({'status': status_value}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'status': 'error', 'message': 'Employee status not found'}, status=status.HTTP_404_NOT_FOUND)
        
class EmployeeStatusUpdateView(APIView):
    def post(self, request):
        employee_id = request.data.get('employee_id')
        is_online = request.data.get('is_online') == True
        try:
            status_obj = Employee.objects.get(employee_id=employee_id)
            status_obj.is_online = is_online
            status_obj.save()
            serializer = EmployeeSerializer(status)
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'status': 'error', 'message': 'Employee status not found'}, status=status.HTTP_404_NOT_FOUND)

class EmployeeCreateView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeRemoveView(APIView):
    def delete(self, request):
        try:
            employee_id = request.GET.get('employee', None)
            if employee_id:
                target = Employee.objects.get(employee_id=employee_id)
                target.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Employee ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        
class PrintEmployeeDetailsView(APIView):
   def get(self, request):
        role = request.GET.get('role', None)
        employee = Employee.objects.filter(role=role)
        response_data = []
        for status in employee:
            response_data.append({
                "id": status.id,
                "employee_id": status.employee_id,
                "name": status.name,
                "email": status.email,
                "contact_number": status.contact_number,
                "password": status.password,
                "status": status.is_online
            })
        return Response(response_data)
