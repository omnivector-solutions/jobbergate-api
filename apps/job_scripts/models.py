from django.db import models

from django.contrib.auth.models import User

from apps.applications.models import Application


class JobScript(models.Model):
    """The job_script table is used to track information
    about job scripts.
    """

    job_script_name = models.CharField(
        max_length=255
    )

    job_script_description = models.CharField(
        max_length=255
    )

    job_script_data_as_string = models.TextField()

    job_script_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="job_scripts",
        related_query_name="job_script",
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
        verbose_name = 'job_script'
        verbose_name_plural = 'job_scripts'
        db_table = 'job_scripts'

    def __str__(self):
        return self.job_script_name

