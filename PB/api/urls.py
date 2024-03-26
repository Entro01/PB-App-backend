# employees/urls.py
from django.urls import path
from .views import LoginView, EmployeeStatusView, EmployeeStatusUpdateView, EmployeeCreateView, PrintEmployeeDetailsView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('employee-status/', EmployeeStatusView.as_view(), name='employee_status'),
    path('employee-status-update/', EmployeeStatusUpdateView.as_view(), name='employee_status_update'),
    path('employee-create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('print-employee-statuses/<str:role>', PrintEmployeeDetailsView.as_view(), name='print_employee_statuses'),
]
