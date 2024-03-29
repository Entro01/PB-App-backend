# employees/urls.py
from django.urls import path
from .views import LoginView, EmployeeStatusView, EmployeeStatusUpdateView, EmployeeCreateView, EmployeeRemoveView, PrintEmployeeDetailsView, EnquiryCreateView, PrintEnquiryDetailsView, UpdateEnquiryStatusView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('employee-status/', EmployeeStatusView.as_view(), name='employee_status'),
    path('employee-status-update/', EmployeeStatusUpdateView.as_view(), name='employee_status_update'),
    path('employee-create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee-remove/', EmployeeRemoveView.as_view(), name='employee_remove'),
    path('print-employee-details/', PrintEmployeeDetailsView.as_view(), name='print_employee_details'),
    path('enquiry-create/', EnquiryCreateView.as_view(), name='enquiry_create'),
    path('print-enquiry-details/', PrintEnquiryDetailsView.as_view(), name='print_enquiry_details'),
    path('update-enquiry-status/', UpdateEnquiryStatusView.as_view(), name='update_enquiry_status'),
]
