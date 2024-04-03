from django.db import models
from django.contrib.postgres.fields import ArrayField

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
    spreadsheet = models.TextField(blank=False, null=False)

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
        ('NEW_INQUIRY', 'Not assigned to any coordinator'),
        ('COORDINATOR_REQUESTED', 'Assigned to a PC but not accepted'),
        ('FREELANCERS_REQUESTED', 'Assigned to a FR but not accepted by at least one fr'),
        ('FREELANCERS_ACCEPTED', 'Assigned to a FR and accepted by at least one fr'),
        ('FREELANCER_FINALIZED', 'Finalized with an fr'),
        ('INQUIRY_RESOLVED', 'Resolved - Check resolve status')
    ]

    RESOLVE_STATUS = [
        ('TIME_ISSUES', 'Time Issues'),
        ('DISTANCE_ISSUES', 'Distance Issues'),
        ('PAYMENT_PENDING', 'Payment Pending'),
        ('ORDER_COMPLETE', 'Order Complete'),
        ('NO_RESPONSE', 'No Response'),
        ('SERVICES_NOT_AVAILABLE', 'Services Not Available'),
        ('RESOLVED', 'Resolved')
    ]
    
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    status = models.CharField(choices=STATUS_CHOICES, default=0)
    coordinator = models.CharField(max_length=255, blank=True, null=True)
    assigned_fr = models.CharField(max_length=255, blank=True, null=True), 
    accepted_fr = models.CharField(max_length=255, blank=True, null=True), 
    final_fr = models.CharField(max_length=255, blank=True, null=True)
    resolve_status = models.CharField(choices=RESOLVE_STATUS)
    wp_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
