from django.db import models

class Employee(models.Model):
    ROLES = [
        ('Admin', 'Admin'),
        ('Project Coordinator', 'Project Coordinator'),
        ('Freelancer', 'Freelancer'),
        ('Accounting', 'Accounting'),
    ]
    employee_id = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=ROLES)
    contact_number = models.CharField(max_length=255)

    def __str__(self):
        return self.employee_id

class EmployeeStatus(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee.employee_id} Status"
