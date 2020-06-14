from django.db import models

from django.contrib.auth.models import User

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
        User,
        on_delete=models.CASCADE
    )

    job_script = models.ForeignKey(
        JobScript,
        on_delete=models.CASCADE,
        related_name="job_submissions",
        related_query_name="job_submission",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'job_submission'
        verbose_name_plural = 'job_submissions'
        db_table = 'job_submissions'

    def __str__(self):
        return self.job_submission_name
