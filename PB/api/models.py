from django.db import models


class Dictionary():
      
      ROLES = [
        ('Admin', 'Admin'),
        ('Coordinator', 'Project Coordinator'),
        ('Freelancer', 'Freelancer'),
        ('Accounting', 'Accounting'),
    ]
      
      STATUS_CHOICES = [
        ('NEW_ENQUIRY', 'Not assigned to any coordinator'),
        ('COORDINATORS_REQUESTED', 'Assigned to a coordinator but not accepted'),
        ('COORDINATOR_FINALIZED', 'Assigned to a PC but not accepted'),
        ('FREELANCERS_REQUESTED', 'Assigned to a FR but not accepted by at least one fr'),
        ('FREELANCERS_ACCEPTED', 'Assigned to a FR and accepted by at least one fr'),
        ('FREELANCER_FINALIZED', 'Finalized with an fr'),
        ('ENQUIRY_RESOLVED', 'Resolved - Check resolve status')
    ]
      
      RESOLVE_TAGS = [
        ('TIME_ISSUES', 'Time Issues'),
        ('DISTANCE_ISSUES', 'Distance Issues'),
        ('PAYMENT_PENDING', 'Payment Pending'),
        ('ORDER_PLACED', 'Order Complete'),
        ('NO_RESPONSE', 'No Response'),
        ('SERVICES_NOT_AVAILABLE', 'Services Not Available'),
        ('RESOLVED', 'Resolved')
    ]

      SERVICES = [
        ('PROJECT', 'Projects Preparation'),
        ('MODELS', 'Models Preparation'),
        ('ACADEMIC_WRITING', 'Academic Writing (Thesis, Dissertation, SOP, etc.)'),
        ('MS_OFFICE', 'MS Office (PPT, Word, Excel)'),
        ('DIY', 'DIY Crafts'),
        ('PAINTING', 'Posters/Painting'),
        ('GRAPHIC', 'Graphic Design'),
        ('PROGRAMMING', 'Programming (Java, Phython, etc.)'),
        ('GRAFFITI', 'Wall Painting / Graffiti'),
        ('HOMEWORK', 'Holidays Homework'),
        ('OTHERS', 'Others')
    ]
      
      ACTIONS = [
        ('COORDINATOR_REQUESTED', 'Request sent to a coordinator'),
        ('COORDINATORS_ACCEPTED', 'Request accepted by a coordinator'),
        ('COORDINATOR_REJECTED', 'Request declined by a coordinator'),
        ('COORDINATOR_TIME_UP', 'Request not accepted in time by a coordinator'),
        ('FREELANCERS_REQUESTED', 'Request sent to a freelancer'),
        ('FREELANCERS_ACCEPTED', 'Request accepted by a freelancer'),
        ('FREELANCERS_REJECTED', 'Request declined by a freelancer'),
        ('FREELANCERS_TIME_UP', 'Request not accepted in time by a freelancer'),
        ('FREELANCERS_FINALIZED', 'A freelancer is finalized to work on the project'),
    ]      


class Employee(models.Model):
    
    employee_id = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, default="1234")
    name = models.CharField(max_length=255, default="null")
    email = models.CharField(max_length=255, default="null") 
    role = models.CharField(max_length=255, choices=Dictionary.ROLES, default = "Freelancer")
    contact_number = models.CharField(max_length=255)
    is_online = models.BooleanField(default=False)
    spreadsheet = models.TextField(blank=False, null=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            role_code = self.employee_id.split('-')[1] if '-' in self.employee_id else None
            if role_code:
                self.role = Dictionary.ROLES.get(role_code, 'Accounting')
        
        self.password = self.contact_number
        
        super(Employee, self).save(*args, **kwargs)

class Enquiry(models.Model):

    name = models.CharField(max_length=255, blank=False, null=False)
    deadline = models.BigIntegerField(blank=False, null=False),
    service = models.CharField(max_length=255, blank=False, null=False),
    description = models.TextField(blank=False, null=False),
    contact_number = models.CharField(max_length=255, blank=False, null=False),
    delivery_area = models.CharField(max_length=255, blank=False, null =False),
    reference = models.TextField(blank=True),
    status = models.CharField(max_length=255, choices=Dictionary.STATUS_CHOICES, default='NEW_ENQUIRY'),
    assigned_coordinators = models.CharField(max_length=255, blank=True, null=True),
    coordinator_timer = models.BigIntegerField(blank=True, null=True),
    coordinator_alloted_time = models.BigIntegerField(blank=True, null=True),
    accepted_coordinator = models.CharField(max_length=255, blank=True, null=True)
    assigned_fr = models.CharField(max_length=255, blank=True, null=True),
    freelancer_timer = models.BigIntegerField(blank=True, null=True),
    freelancer_alloted_time = models.BigIntegerField(blank=True, null=True),
    accepted_fr = models.CharField(max_length=255, blank=True, null=True), 
    final_fr = models.CharField(max_length=255, blank=True, null=True)
    resolve_status = models.CharField(max_length=255, choices=Dictionary.RESOLVE_TAGS, null=True)
    wp_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
