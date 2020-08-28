# Generated by Django 3.0.7 on 2020-08-27 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='application_dir_listing',
        ),
        migrations.RemoveField(
            model_name='application',
            name='application_dir_listing_acquired',
        ),
        migrations.RemoveField(
            model_name='application',
            name='application_location',
        ),
        migrations.AlterField(
            model_name='application',
            name='application_description',
            field=models.TextField(default=''),
        ),
    ]