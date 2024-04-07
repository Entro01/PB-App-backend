# employees/views.pys import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Enquiry
from .serializers import EmployeeSerializer, EnquirySerializer
from .models import Dictionary

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
            employee_id = request.GET.get('employee_id', None)
            if employee_id:
                target = Employee.objects.get(employee_id=employee_id)
                target.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Employee ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        
class PrintEmployeeDetailsView(APIView):
    def get(self, request):
        arg = request.GET.get('role_or_employee_id', None)
        response_data = []

        if arg is None:
            employee = Employee.objects.all()
        elif arg in [choice[0] for choice in Dictionary.ROLES]:
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
    
class EmployeeSpreadsheetView(APIView):
    def get(self, request):
        employee_id = request.GET.get('employee_id', None)
        try:
            spreadhseet = Employee.objects.get(employee_id=employee_id).spreadsheet
            return Response({'link': spreadhseet}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'status': 'error', 'message': 'Employee spreadsheet not found'}, status=status.HTTP_404_NOT_FOUND)
        
class EnquiryCreateView(APIView):
    def post(self, request):
        serializer = EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PrintEnquiryDetailsView(APIView):
    def get(self, request):
        employee_id = request.GET.get('employee_id', None)
        status_val = request.GET.get('status', None)

        if not employee_id:
            return Response({'status': 'error', 'message': 'EmployeeID is required'}, status=status.HTTP_404_NOT_FOUND)

        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response({'status': 'error', 'message': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        if status_val is not None:
            if status_val not in [choice[0] for choice in Dictionary.STATUS_CHOICES]:
                return Response({'status': 'error', 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        role_mapping = {
            'AM': 'Admin',
            'FR': 'Freelancer',
            'PC': 'Coordinator'
        }
        role = role_mapping.get(employee_id.split('-')[1], None)

        if not role:
            return Response({'status': 'error', 'message': 'Invalid employee ID format'}, status=status.HTTP_404_NOT_FOUND)

        if role == 'Admin':
            if status_val:
                enquiries = Enquiry.objects.filter(status=status_val)
            else:
                enquiries = Enquiry.objects.all()
        elif role == 'Coordinator':
            if status_val:
                enquiries = Enquiry.objects.filter(assigned_coordinator__contains=employee_id, status=status_val)
            else:
                enquiries = Enquiry.objects.filter(assigned_coordinator__contains=employee_id)
        elif role == 'Freelancer':
            if status_val:
                enquiries = Enquiry.objects.filter(assigned_fr__contains=employee_id, status=status_val)
            else:
                enquiries = Enquiry.objects.filter(assigned_fr__contains=employee_id)

        if role == 'Freelancer':
            return Response(list(enquiries.values('name', 'deadline', 'service', 'description', 'reference', 'accepted_coordinator', 'wp_link')), status=status.HTTP_200_OK)
        elif role == 'Coordinator':
            return Response(list(enquiries.values('name', 'deadline', 'service', 'description', 'contact_number', 'reference', 'status', 'assigned_fr', 'accepted_fr', 'wp_link')), status=status.HTTP_200_OK)
        else:
            return Response(list(enquiries.values()), status=status.HTTP_200_OK)

class UpdateEnquiryStatusView(APIView):
    def post(self, request):
        enquiry_id = request.data.get('enquiry_id')
        action = request.data.get('action')
        employee_id = request.data.get('employee_id')
        time = request.data.get('time')
        alloted_time = request.data.get('alloted time')

        try:
            enquiry = Enquiry.objects.get(id=enquiry_id)
        except Enquiry.DoesNotExist:
            return Response({"error": "Enquiry not found"}, status=status.HTTP_404_NOT_FOUND)

        if action not in [choice[0] for choice in Dictionary.ACTIONS]:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        if action in ['COORDINATOR_REQUESTED', 'COORDINATORS_ACCEPTED', 'COORDINATOR_REJECTED', 'COORDINATOR_TIME_UP']:
            if employee.role != 'Coordinator':
                return Response({"error": "Employee is not a coordinator"}, status=status.HTTP_400_BAD_REQUEST)
        elif action in ['FREELANCERS_REQUESTED', 'FREELANCERS_ACCEPTED', 'FREELANCERS_REJECTED', 'FREELANCERS_TIME_UP', 'FREELANCERS_FINALIZED']:
            if employee.role != 'Freelancer':
                return Response({"error": "Employee is not a freelancer"}, status=status.HTTP_400_BAD_REQUEST)
        
        if action == 'COORDINATORS_REQUESTED':
            if time or alloted_time is None:
                return Response({"error": "Either Current Time or Alloted Time not found"}, status=status.HTTP_400_BAD_REQUEST)
            enquiry.assigned_coordinator = f"{enquiry.assigned_coordinator} {employee_id}" if enquiry.assigned_coordinator else employee_id
            enquiry.status = 'COORDINATOR_REQUESTED'
            enquiry.coordinator_timer = time
            enquiry.coordinator_alloted_time = alloted_time
        elif action == 'COORDINATORS_ACCEPTED':
            enquiry.accepted_coordinator = employee_id
            enquiry.status = 'COORDINATOR_FINALIZED'
        elif action == 'COORDINATOR_REJECTED' or action == 'COORDINATOR_TIME_UP':
                enquiry.status = 'NEW_ENQUIRY'
        elif action == 'FREELANCERS_REQUESTED':
            if time or alloted_time is None:
                return Response({"error": "Either Current Time or Alloted Time not found"}, status=status.HTTP_400_BAD_REQUEST)
            enquiry.assigned_fr = f"{enquiry.assigned_fr} {employee_id}" if enquiry.assigned_fr else employee_id
            enquiry.status = 'FREELANCERS_REQUESTED'
            enquiry.freelancer_timer = time
            enquiry.freelancer_alloted_time = alloted_time
        elif action == 'FREELANCERS_ACCEPTED':
            enquiry.accepted_fr = f"{enquiry.accepted_fr} {employee_id}" if enquiry.accepted_fr else employee_id
            enquiry.status = 'FREELANCERS_ACCEPTED'
        elif action == 'FREELANCERS_REJECTED' or action == 'FREELANCERS_TIME_UP':
            if not enquiry.assigned_fr or not enquiry.accepted_fr:
                enquiry.status = 'COORDINATORS_FINALIZED'
        elif action == 'FREELANCERS_FINALIZED':
            enquiry.final_fr = f"{enquiry.final_fr} {employee_id}" if enquiry.final_fr else employee_id
            enquiry.status = 'FREELANCERS_FINALIZED'

        enquiry.save()
        return Response({"message": "Enquiry status updated successfully"}, status=status.HTTP_200_OK)

class CheckTimeView(APIView):
    def get(self, request):
        enquiry_id = request.data.get('enquiry_id', None)
        role = request.data.get('role', None)

        if not enquiry_id:
            return Response({'error': 'enquiry_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            enquiry = Enquiry.objects.get(id=enquiry_id)
            if role == 'Coordinator':
                time = enquiry.coordinator_timer
                alloted_time = enquiry.coordinator_alloted_time
            elif role == 'Freelancer':
                time = enquiry.freelancer_timer
                alloted_time = enquiry.freelancer_alloted_time
            else:
                return Response({'error:' 'Wrong role'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'time': time, 'alloted_time': alloted_time}, status=status.HTTP_200_OK)
        except Enquiry.DoesNotExist:
            return Response({'error': 'Enquiry not found'}, status=status.HTTP_404_NOT_FOUND)

class UpdateEnquiryWithWPLinkView(APIView):
    def post(self, request):
        enquiry_id = request.data.get('enquiry_id', None)
        wp_link = request.data.get('wp_link', None)
        
        if not wp_link:
            return Response({'error': 'wp_link is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            enquiry = Enquiry.objects.get(id=enquiry_id)
        except Enquiry.DoesNotExist:
            return Response({'error': 'Enquiry not found'}, status=status.HTTP_404_NOT_FOUND)

        enquiry.wp_link = wp_link
        enquiry.save()
        return Response({'message': 'Enquiry updated successfully'}, status=status.HTTP_200_OK)

class CloseEnquiryView(APIView):
    def post(self, request):
        enquiry_id = request.data.get('enquiry_id')
        resolve_tag = request.data.get('resolve_tag')
        
        if not enquiry_id:
            return Response({'error': 'enquiry_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            enquiry = Enquiry.objects.get(id=enquiry_id)
        except Enquiry.DoesNotExist:
            return Response({'error': 'Enquiry not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not resolve_tag:
            return Response({'error': 'resolve_tag is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if resolve_tag not in [choice[0] for choice in Dictionary.RESOLVE_TAGS]:
            return Response({'error': 'Invalid resolve tag'}, status=status.HTTP_400_BAD_REQUEST)

        enquiry.status = 'ENQUIRY_RESOLVED'
        enquiry.resolve_status = resolve_tag
        enquiry.save()
        return Response({'message': 'Enquiry closed successfully'}, status=status.HTTP_200_OK)
