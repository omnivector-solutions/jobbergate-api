from django.db import models

from django.contrib.auth.models import User


class JobSubmission(models.Model):
    job_submission_name = models.CharField(max_length=255)
    job_submission_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    job_submission = models.CharField(max_length=1000)


