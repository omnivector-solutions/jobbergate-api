from rest_framework import mixins, viewsets, permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from apps.job_submissions.models import JobSubmission
from apps.job_submissions.serializers import JobSubmissionSerializer

class JobSubmissionListView(generics.ListCreateAPIView):
    """
    list view for 'job-submission/'
    """
    queryset = JobSubmission.objects.all()
    serializer_class = JobSubmissionSerializer

    def delete(self, request, JobSubmission_pk, format=None):
        jobscript = JobSubmission.objects.get(id=JobSubmission_pk)
        jobscript.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobSubmissionView(generics.RetrieveUpdateDestroyAPIView):
    '''
    detail view for 'job-submission/<int:pk>'
    '''
    serializer_class = JobSubmissionSerializer
    queryset = JobSubmission.objects.all()
