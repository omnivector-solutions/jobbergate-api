from django.conf import settings
from django.db import models

from apps.job_scripts.models import JobScript


class JobSubmission(models.Model):
    """The job_submission table is used to track information
    about job submissions.
    """

    job_submission_name = models.CharField(
        max_length=255,
    )

    job_submission_description = models.CharField(
        max_length=255,
    )

    job_submission_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    job_script = models.ForeignKey(
        JobScript,
        on_delete=models.CASCADE,
        related_name="job_submissions",
        related_query_name="job_submission",
    )

    slurm_job_id = models.TextField(default="")

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        verbose_name = "job_submission"
        verbose_name_plural = "job_submissions"
        db_table = "job_submissions"

    def __str__(self):
        return self.job_submission_name
