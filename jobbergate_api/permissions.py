from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group

class ViewObject(BasePermission):
    """
    Only person who assigned has permission
    """

    def has_object_permission(self, user):
        # check if user who launched request is object owner
        group  = user.groups.get(name="test_permissions")
        if group in user.groups:
            return True
        else:
            return False
