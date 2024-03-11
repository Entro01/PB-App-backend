from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee, EmployeeStatus

@receiver(post_save, sender=Employee)
def create_employee_status(sender, instance, created, **kwargs):
    if created:
        EmployeeStatus.objects.create(employee=instance, is_online=False)
