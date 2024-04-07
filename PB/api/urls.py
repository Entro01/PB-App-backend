# employees/urls.py
from django.urls import path
from .views import LoginView, EmployeeStatusView, EmployeeStatusUpdateView, EmployeeCreateView, EmployeeRemoveView, EmployeeSpreadsheetView, PrintEmployeeDetailsView, EnquiryCreateView, PrintEnquiryDetailsView, UpdateEnquiryStatusView, CheckTimeView, UpdateEnquiryWithWPLinkView, CloseEnquiryView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('employee-status/', EmployeeStatusView.as_view(), name='employee_status'),
    path('employee-status-update/', EmployeeStatusUpdateView.as_view(), name='employee_status_update'),
    path('employee-create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee-remove/', EmployeeRemoveView.as_view(), name='employee_remove'),
    path('print-employee-details/', PrintEmployeeDetailsView.as_view(), name='print_employee_details'),
    path('employee-spreadsheet/', EmployeeSpreadsheetView.as_view(), name='employee_spreadsheet'),
    path('enquiry-create/', EnquiryCreateView.as_view(), name='enquiry_create'),
    path('print-enquiry-details/', PrintEnquiryDetailsView.as_view(), name='print_enquiry_details'),
    path('update-enquiry-status/', UpdateEnquiryStatusView.as_view(), name='update_enquiry_status'),
    path('check-time/', CheckTimeView.as_view(), name='check_time'),
    path('update-enquiry-wp-link/', UpdateEnquiryWithWPLinkView.as_view(), name='update-enquiry-wp-link'),
    path('close-enquiry/', CloseEnquiryView.as_view(), name='close-enquiry'),
]
