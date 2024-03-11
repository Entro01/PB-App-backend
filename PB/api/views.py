from rest_framework import generics, permissions
from .models import Employee, EmployeeStatus
from .serializers import EmployeeSerializer, EmployeeStatusSerializer
from .authentication import EmployeeIDAuthentication

class EmployeeLoginView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [EmployeeIDAuthentication]
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        employee = serializer.save()
        print(f"Employee {employee.employee_id} logged in at {datetime.now()}")

class EmployeeStatusUpdateView(generics.UpdateAPIView):
    queryset = EmployeeStatus.objects.all()
    serializer_class = EmployeeStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.employeestatus

class EmployeeStatusListView(generics.ListAPIView):
    queryset = EmployeeStatus.objects.all()
    serializer_class = EmployeeStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
