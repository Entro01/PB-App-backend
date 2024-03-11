from django.urls import path
from .views import EmployeeLoginView, EmployeeStatusUpdateView, EmployeeStatusListView

urlpatterns = [
    path('login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('status/update/', EmployeeStatusUpdateView.as_view(), name='employee-status-update'),
    path('status/', EmployeeStatusListView.as_view(), name='employee-status-list'),
]
