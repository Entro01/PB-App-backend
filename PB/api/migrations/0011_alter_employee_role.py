# Generated by Django 5.0.3 on 2024-03-28 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_enquiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Coordinator', 'Project Coordinator'), ('Freelancer', 'Freelancer'), ('Accounting', 'Accounting')], default='Freelancer', max_length=255),
        ),
    ]
