# Generated by Django 5.0.3 on 2024-03-17 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_employee_address_remove_employee_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeestatus',
            name='employee',
        ),
        migrations.AddField(
            model_name='employeestatus',
            name='employee_id',
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
