# employees/urls.py
from django.urls import path
from .views import LoginView, EmployeeStatusView, EmployeeStatusUpdateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('employee-status/', EmployeeStatusView.as_view(), name='employee_status'),
    path('employee-status-update/', EmployeeStatusUpdateView.as_view(), name='employee_status_update'),
]
