from django.db import models

from django.contrib.auth.models import User


class JobScript(models.Model):
    job_script_name = models.CharField(max_length=255)
    job_script_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    job_script = models.CharField(max_length=1000)


