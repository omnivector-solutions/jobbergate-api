# Generated by Django 3.0.7 on 2020-06-15 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job_scripts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_submission_name', models.CharField(max_length=255)),
                ('job_submission_description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job_script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_submissions', related_query_name='job_submission', to='job_scripts.JobScript')),
                ('job_submission_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'job_submission',
                'verbose_name_plural': 'job_submissions',
                'db_table': 'job_submissions',
            },
        ),
    ]
