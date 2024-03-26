from django.db import models

class Employee(models.Model):
    ROLES = [
        ('Admin', 'Admin'),
        ('Project Coordinator', 'Project Coordinator'),
        ('Freelancer', 'Freelancer'),
        ('Accounting', 'Accounting'),
    ]
    employee_id = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, default="1234")
    name = models.CharField(max_length=255, default="null")
    email = models.CharField(max_length=255, default="null") 
    role = models.CharField(max_length=255, choices=ROLES)
    contact_number = models.CharField(max_length=255)
    is_online = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Set the password to the contact number before saving
        self.password = self.contact_number
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.employee_id