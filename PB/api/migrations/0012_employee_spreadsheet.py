# Generated by Django 5.0.3 on 2024-03-29 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_employee_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='spreadsheet',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
