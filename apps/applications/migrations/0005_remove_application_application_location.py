# Generated by Django 3.0.7 on 2020-08-28 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0004_application_application_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='application_location',
        ),
    ]
