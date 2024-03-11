from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    EMPLOYEE_ROLES = (
        ('AM', 'Admin'),
        ('PC', 'Project Coordinator'),
        ('FR', 'Freelancer'),
        ('AC', 'Accounting'),
    )

    employee_id = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=2, choices=EMPLOYEE_ROLES, default='FR')
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.employee_id

    def save(self, *args, **kwargs):
        # Extract the role code from the employee_id
        self.role = self.employee_id[3:5]
        super().save(*args, **kwargs)
