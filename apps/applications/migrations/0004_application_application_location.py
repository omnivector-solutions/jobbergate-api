# Generated by Django 3.0.7 on 2020-08-28 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_auto_20200827_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='application_location',
            field=models.TextField(default='', max_length=255),
        ),
    ]
