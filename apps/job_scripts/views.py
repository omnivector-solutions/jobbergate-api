from django.shortcuts import render
    permissions,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from apps.job_scripts.models import JobScript
from apps.job_scripts.serializers import JobScriptSerializer


class JobScriptListView(APIView):
    """List job scripts owned by the authenticated user.

    * Requires token authentication.

    endpoint: job-scripts/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobScriptSerializer
    queryset = JobScript.objects.all()

    def get(self, request):
        user = request.user
        job_scripts = JobScript.objects.get(user=user)
        serializer = JobScriptSerializer(data=job_scripts, many=True)

        print(serializer.__dict__)
        return Response(JSONRenderer().render(serializer.data))


class JobScriptDetailView(APIView):
    """Job script get, post, update, delete operations.

    * Requires token authentication.

    endpoint: job-scripts/<pk>/
    """
