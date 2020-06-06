from rest_framework import (
    permissions,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from apps.job_submissions.models import JobSubmission
from apps.job_submissions.serializers import JobSubmissionSerializer


class JobSubmissionListView(APIView):
    """List job submissions owned by the authenticated user.

    * Requires token authentication.

    endpoint: job-submissions/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobSubmissionSerializer
    queryset = JobSubmission.objects.all()

    def get(self, request):
        user = request.user
        job_submissions = JobSubmission.objects.get(user=user)
        serializer = JobSubmissionSerializer(data=job_scripts, many=True)

        print(serializer.__dict__)
        return Response(JSONRenderer().render(serializer.data))


class JobSubmissionDetailView(APIView):
    """Job submit get, post, update, delete.

    * Requires token authentication.

    endpoint: job-submissions/<pk>/
    """
