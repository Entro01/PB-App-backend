from django.db import models

class Employee(models.Model):
    ROLES = [
        ('Admin', 'Admin'),
        ('Coordinator', 'Project Coordinator'),
        ('Freelancer', 'Freelancer'),
        ('Accounting', 'Accounting'),
    ]
    employee_id = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, default="1234")
    name = models.CharField(max_length=255, default="null")
    email = models.CharField(max_length=255, default="null") 
    role = models.CharField(max_length=255, choices=ROLES, default = "Freelancer")
    contact_number = models.CharField(max_length=255)
    is_online = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            role_code = self.employee_id.split('-')[1] if '-' in self.employee_id else None
            if role_code:
                role_mapping = {
                    'AM': 'Admin',
                    'PC': 'Coordinator',
                    'FR': 'Freelancer',
                }
                self.role = role_mapping.get(role_code, 'Accounting')
        
        self.password = self.contact_number
        
        super(Employee, self).save(*args, **kwargs)

    
class Enquiry(models.Model):
    STATUS_CHOICES = [
        (0, 'Unassigned'),
        (1, 'Assigned to a PC but not accepted'),
        (2, 'Assigned to a FR but not accepted'),
        (3, 'Assigned to a FR and accepted'),
        (4, 'Completed'),
    ]

    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    coordinator = models.CharField(max_length=255, blank=True, null=True)
    freelancer = models.CharField(max_length=255, blank=True, null=True)
    repo_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
