from django.core.management.base import BaseCommand
from django.db.models import Q
import csv
import os

from api.models import Employee, Enquiry

class Command(BaseCommand):
    help = 'Exports Employee and Enquiry data to CSV files'

    def handle(self, *args, **options):
        employee_csv_path = os.path.join("C:/Users/shubh/Documents/PB-store", 'employees.csv')
        enquiry_csv_path = os.path.join("C:/Users/shubh/Documents/PB-store", 'enquiries.csv')
        
        with open(employee_csv_path, 'w', newline='') as csvfile:
            fieldnames = ['employee_id', 'password', 'name', 'email', 'role', 'contact_number', 'is_online']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for employee in Employee.objects.all():
                writer.writerow({
                    'id': employee.id,
                    'employee_id': employee.employee_id,
                    'password': employee.password,
                    'name': employee.name,
                    'email': employee.email,
                    'role': employee.get_role_display(),
                    'contact_number': employee.contact_number,
                    'is_online': employee.is_online,
                })

        with open(enquiry_csv_path, 'w', newline='') as csvfile:
            fieldnames = ['name', 'description', 'status', 'coordinator', 'freelancer', 'repo_link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for enquiry in Enquiry.objects.all():
                writer.writerow({
                    'id': enquiry.id,
                    'name': enquiry.name,
                    'description': enquiry.description,
                    'status': enquiry.get_status_display(),
                    'coordinator': enquiry.coordinator,
                    'freelancer': enquiry.freelancer,
                    'repo_link': enquiry.repo_link,
                })

        self.stdout.write(self.style.SUCCESS('Data exported successfully'))
