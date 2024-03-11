from django.urls import path
from .views import EmployeeLoginView, EmployeeStatusUpdateView, EmployeeStatusListView, EmployeeCreateView

urlpatterns = [
    path('login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('status/update/', EmployeeStatusUpdateView.as_view(), name='employee-status-update'),
    path('status/', EmployeeStatusListView.as_view(), name='employee-status-list'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
]
