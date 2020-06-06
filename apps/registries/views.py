from rest_framework import (
    permissions,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from apps.registries.models import Registry
from apps.registries.serializers import RegistrySerializer


class RegistryListView(APIView):
    """List registries owned by the authenticated user.

    * Requires token authentication.

    endpoint: registries/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegistrySerializer
    queryset = Registry.objects.all()

    def get(self, request):
        user = request.user
        job_scripts = JobScript.objects.get(user=user)
        serializer = JobScriptSerializer(data=job_scripts, many=True)

        print(serializer.__dict__)
        return Response(JSONRenderer().render(serializer.data))


class RegistryDetailView(APIView):
    """Registry get, post, update, delete.

    * Requires token authentication.

    endpoint: registries/<pk>/
    """
