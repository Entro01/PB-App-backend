# employees/views.py
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Employee, EmployeeStatus
from django.shortcuts import render

class LoginView(View):
    def get(self, request, *args, **kwargs):
        # Render the login form
        return render(request, 'registration/login.html')

    def post(self, request, *args, **kwargs):
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            if employee.contact_number == password:
                user = User.objects.create_user(username=employee_id, password=password)
                login(request, user)
                return JsonResponse({'status': 'success', 'role': employee.role})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Employee not found'})

class EmployeeStatusView(View):
    def get(self, request, *args, **kwargs):
        employee_id = request.GET.get('employee_id')
        try:
            status = EmployeeStatus.objects.get(employee__employee_id=employee_id).is_online
            return JsonResponse({'status': status})
        except EmployeeStatus.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Employee status not found'})

    def post(self, request, *args, **kwargs):
        employee_id = request.POST.get('employee_id')
        is_online = request.POST.get('is_online') == '1'
        try:
            status = EmployeeStatus.objects.get(employee__employee_id=employee_id)
            status.is_online = is_online
            status.save()
            return JsonResponse({'status': 'success'})
        except EmployeeStatus.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Employee status not found'})
