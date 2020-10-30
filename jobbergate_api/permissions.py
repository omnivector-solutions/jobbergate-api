from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group

class ViewObject(BasePermission):
    """
    Only person who assigned has permission
    """

    def has_object_permission(self, request, view, obj):
        # check if user who launched request is object owner
        user = request.user
        print("in test_permissions ?")
        test_grp = user.groups.filter(name='test_permissions').exists()
        print(test_grp)
        print("in test_perm2 ?")
        test_grp2 = user.groups.filter(name='test_perm2').exists()
        print(test_grp2)
        if user.groups.filter(name='test_permissions').exists():
            return True
        else:
            return False
