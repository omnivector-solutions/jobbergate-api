from django.db import models

from django.contrib.auth.models import User


class Application(models.Model):
    application_name = models.CharField(max_length=255)
    application_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.CharField(max_length=1000)


