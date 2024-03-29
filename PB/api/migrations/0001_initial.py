# Generated by Django 5.0.3 on 2024-03-11 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=15, unique=True)),
                ('role', models.CharField(choices=[('AM', 'Admin'), ('PC', 'Project Coordinator'), ('FR', 'Freelancer'), ('AC', 'Accounting')], default='FR', max_length=2)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('pincode', models.CharField(max_length=6)),
            ],
        ),
    ]
