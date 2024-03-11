from django.contrib.auth.models import User
from rest_framework import authentication, exceptions

class EmployeeIDAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        employee_id = request.data.get('employee_id')
        contact_number = request.data.get('contact_number')

        if not employee_id or not contact_number:
            return None

        try:
            user = User.objects.get(employee_id=employee_id)
            if user.profile.contact_number != contact_number:
                raise exceptions.AuthenticationFailed('Incorrect contact number.')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such employee.')

        return (user, None)
