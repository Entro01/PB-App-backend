from django.db import models

class Employee(models.Model):
    EMPLOYEE_ROLES = (
        ('AM', 'Admin'),
        ('PC', 'Project Coordinator'),
        ('FR', 'Freelancer'),
        ('AC', 'Accounting'),
    )

    employee_id = models.CharField(max_length=15, unique=True)
    name = models.TextField(default='nill')
    role = models.CharField(max_length=2, choices=EMPLOYEE_ROLES, default='FR')
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.employee_id

class EmployeeStatus(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee.employee_id} - {self.is_online}"
