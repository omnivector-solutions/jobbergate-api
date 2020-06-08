from django.db import models

from django.contrib.auth.models import User


class Registry(models.Model):
    registry_owner = models.ForeignKey(User, on_delete=models.CASCADE)
