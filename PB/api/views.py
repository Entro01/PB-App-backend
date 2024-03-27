# employees/views.pys import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Enquiry
from .serializers import EmployeeSerializer, EnquirySerializer

class LoginView(APIView):
    def post(self, request):
        employee_id = request.data.get('employee_id')
        password = request.data.get('password')
        try:
            employee = Employee.objects.get(employee_id=employee_id) 
            if employee.contact_number == password:
                return Response({'status': 'success', 'role': employee.role}, status=status.HTTP_200_OK)
            else:
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
        arg = request.GET.get('arg', None)
        response_data = []

        roles = ('Admin', 'Project Coordinator', 'Freelancer', 'Accounting')

        if arg is None:
            employee = Employee.objects.all()
        elif arg in roles:
            employee = Employee.objects.filter(role=arg)
        else:
            try:
                employee_id = arg
                employee = Employee.objects.filter(employee_id=employee_id)
            except ValueError:
                return Response({'status': 'error', 'message': 'Invalid role or employee ID'}, status=400)
        for status in employee:
            response_data.append({
                "id": status.id,
                "employee_id": status.employee_id,
                "name": status.name,
                "email": status.email,
                "contact_number": status.contact_number,
                "status": status.is_online
            })

        return Response(response_data)
    
class EnquiryCreateView(APIView):
    def post(self, request):
        serializer = EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PrintEnquiryDetailsView(APIView):
    def get(self, request):
        employee_id = request.GET.get('arg1', None)
        status_val = request.GET.get('arg2', None)

        if status_val is not None:
            try:
                status_val = int(status_val)
                if status_val < 0 or status_val > 4:
                    return Response({'status': 'error', 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'status': 'error', 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        if not employee_id:
            return Response({'status': 'error', 'message': 'Invalid arguments'}, status=status.HTTP_404_NOT_FOUND)

        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response({'status': 'error', 'message': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        role_mapping = {
            'AM': 'Admin',
            'FR': 'Freelancer',
            'PC': 'Project Coordinator'
        }
        role = role_mapping.get(employee_id.split('-')[1], None)

        if not role:
            return Response({'status': 'error', 'message': 'Invalid employee ID format'}, status=status.HTTP_404_NOT_FOUND)

        if role == 'Admin':
            if status_val:
                enquiries = Enquiry.objects.filter(status=status_val)
            else:
                enquiries = Enquiry.objects.all()
        elif role == 'Project Coordinator':
            if status_val:
                enquiries = Enquiry.objects.filter(coordinator=employee, status=status_val)
            else:
                enquiries = Enquiry.objects.filter(coordinator=employee)
        elif role == 'Freelancer':
            if status:
                enquiries = Enquiry.objects.filter(freelancer=employee, status=status_val)
            else:
                enquiries = Enquiry.objects.filter(freelancer=employee)
        else:
            return Response({'status': 'error', 'message': 'Invalid role'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'enquiries': list(enquiries.values())}, status=status.HTTP_200_OK)