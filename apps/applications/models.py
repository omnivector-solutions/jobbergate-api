from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Application(models.Model):
    """The application table is used to track information
    about jobbergate applications.
    """

    application_name = models.CharField(
        max_length=255,
    )

    application_description = models.TextField(
        default="",
    )

    application_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    application_file = models.TextField(
    )

    application_config = models.TextField(
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
        verbose_name = 'application'
        verbose_name_plural = 'applications'
        db_table = 'applications'
        permissions = (
            ('view_obj', 'Can view object'),
        )

    def __str__(self):
        return self.application_name

    @property
    def application_location(self):
        return f"{settings.S3_BASE_PATH}/{str(self.application_owner_id)}/applications/{str(self.id)}/jobbergate.tar.gz" # noqa
