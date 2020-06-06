from django.db import models

from django.contrib.auth.models import User


class JobScript(models.Model):
    job_script_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
