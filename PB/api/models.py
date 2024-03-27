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
    
class Enquiry(models.Model):
    STATUS_CHOICES = [
        (0, 'Unassigned'),
        (1, 'Assigned to a PC but not accepted'),
        (2, 'Assigned to a PC and accepted'),
        (3, 'Assigned to a FR but not accepted'),
        (4, 'Assigned to a FR and accepted'),
        (5, 'Completed'),
    ]

    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    coordinator = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='coordinated_enquiries')
    freelancer = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='freelanced_enquiries')
    repo_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
